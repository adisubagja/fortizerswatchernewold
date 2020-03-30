# We're using prebuilt docker images
FROM dasbastard/jnckdclxvi:latest

#
# Clone repo and prepare working directory
#
RUN git clone -b test https://github.com/AnggaR96s/dirtybotx2.git /root/emilia
RUN mkdir /root/emilia/bin/
WORKDIR /root/emilia/

CMD ["python3","-m","emilia"]
