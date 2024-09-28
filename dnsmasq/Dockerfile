FROM alpine:edge

RUN apk --no-cache add dnsmasq \
    && mkdir -p /etc/dnsmasq.d/

ADD dnsmasq.conf /etc/

EXPOSE 53 53/udp

ENTRYPOINT ["dnsmasq", "-d"]
