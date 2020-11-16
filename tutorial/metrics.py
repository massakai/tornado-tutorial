import threading
import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta

from prometheus_client.metrics import Summary
from prometheus_client.registry import REGISTRY


@dataclass()
class Sample:
    amount: float
    timestamp: datetime

    def __init__(self, amount=0.0, timestamp: datetime = None):
        self.amount = amount
        if timestamp:
            self.timestamp = timestamp
        else:
            # ロード時の時刻になってしまうので、デフォルト引数にはしない
            self.timestamp = datetime.now()


class _SampleCleaner(threading.Thread):
    """SummaryWithQuantileの有効期限切れサンプルを非同期に掃除するクラス

    メトリクスのリクエストがないとサンプルが溜まり続けるのもよろしくないので、別スレッドで掃除する
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._metrics = []
        self._sleep_time = timedelta(seconds=30)

    def append(self, metric):
        self._metrics.append(metric)

    def update_sleep_time(self, sleep_time: timedelta) -> None:
        self._sleep_time = sleep_time

    def run(self) -> None:
        while True:
            for metric in self._metrics:
                metric.purge()
            time.sleep(self._sleep_time.total_seconds())


_SAMPLE_CLEANER = _SampleCleaner(daemon=True)
_SAMPLE_CLEANER.start()


class SummaryWithQuantile(Summary):
    """QuantileをサポートするSummary
    """

    def __init__(self,
                 name,
                 documentation,
                 labelnames=(),
                 namespace='',
                 subsystem='',
                 unit='',
                 registry=REGISTRY,
                 labelvalues=None,
                 quantiles=None,
                 period: timedelta = timedelta(minutes=5),
                 ):
        # validation
        SummaryWithQuantile._validate_quantiles(quantiles)

        super().__init__(name, documentation, labelnames, namespace, subsystem, unit, registry, labelvalues)
        self._kwargs = {
            'quantiles': quantiles,
            'period': period,
        }
        self._period = period
        self._quantiles = quantiles
        self._observed_deque = deque()
        self._purge_lock = threading.Lock()

        _SAMPLE_CLEANER.append(self)

    @staticmethod
    def _validate_quantiles(quantiles):
        if quantiles is None:
            return

        for quantile in quantiles:
            if quantile < 0:
                raise ValueError(
                    f"Invalid value {quantile} was found in the argument 'quantiles'. "
                    f"Values in 'quantiles' must be greater than or equal to 0.")
            elif quantile >= 1.0:
                raise ValueError(
                    f"Invalid value {quantile} was found in the argument 'quantiles'. "
                    f"Values in 'quantiles' must be less than 1.")

    def observe(self, amount) -> None:
        """メトリクスを観測する

        処理を重くしないこと
        """
        super().observe(amount)
        # 新しいサンプルが先頭になるように追加する
        self._observed_deque.appendleft(Sample(amount))

    def _child_samples(self):
        """可視化項目を生成する

        :return: tuple
        """
        samples = super()._child_samples()
        if self._quantiles:
            now = datetime.now()
            amounts = sorted([sample.amount for sample in self._observed_deque
                              if now - sample.timestamp < self._period])
            period = str(self._period.total_seconds())

            samples = super()._child_samples()
            count = len(amounts)
            samples += (("_sample", {"period": period}, count),)
            if amounts:
                samples += tuple([(
                    "",
                    {"period": period, "quantile": str(quantile)},
                    amounts[int(count * quantile)])
                    for quantile in self._quantiles])
        return samples

    def purge(self) -> None:
        """期限切れになったサンプルをパージする"""
        # 期限確認とpopの間でスレッドが切り替わると、有効なサンプルを取り除いてしまう可能性があるためロックをかける
        if not self._purge_lock.acquire(blocking=False):
            # 他からpurge()が呼ばれているので何もしないで終了
            return

        try:
            now = datetime.now()
            while self._observed_deque:
                # _samplesには新しい順にsampleが入っている
                # 最後の要素が有効期間内であればパージ完了
                if now - self._observed_deque[-1].timestamp < self._period:
                    break
                self._observed_deque.pop()
        finally:
            self._purge_lock.release()
