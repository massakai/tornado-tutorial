ARG PYTHOD_TAG=3.9.0-alpine
FROM python:${PYTHOD_TAG} AS build-env
# FROMの上に書くと読み込まれない
ARG PACKAGE_PATH=/tmp/tornado-tutorial.tgz
COPY . /tmp/
WORKDIR /tmp
RUN python3 setup.py sdist
RUN mv /tmp/dist/tornado-tutorial-*.tar.gz ${PACKAGE_PATH}

FROM python:${PYTHOD_TAG}
# build-envと同じ変数, 値だが書く必要がある
ARG PACKAGE_PATH=/tmp/tornado-tutorial.tgz
COPY --from=build-env ${PACKAGE_PATH} ${PACKAGE_PATH}
RUN pip install ${PACKAGE_PATH}
ENTRYPOINT ["tutorial_server"]
