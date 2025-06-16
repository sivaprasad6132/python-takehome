# -------- Stage 1: Build nsjail --------
FROM debian:bookworm-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential \
    libprotobuf-dev protobuf-compiler \
    libnl-route-3-dev \
    libcap-dev libseccomp-dev \
    libtool autoconf bison flex ca-certificates pkg-config \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail.git /nsjail && \
    cd /nsjail && make

# -------- Stage 2: Final Runtime --------
FROM python:3.10-slim

# Install runtime dependencies for nsjail
RUN apt-get update && apt-get install -y --no-install-recommends \
    libprotobuf32 libnl-route-3-200 libcap2 libseccomp2 \
    && rm -rf /var/lib/apt/lists/*

# Copy nsjail binary from builder
COPY --from=builder /nsjail/nsjail /usr/bin/nsjail

# Setup app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
