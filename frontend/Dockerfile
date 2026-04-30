FROM oven/bun:1 AS development

WORKDIR /frontend

COPY ./ ./
RUN bun install --frozen-lockfile
CMD [ "bun", "run", "dev", "--host", "0.0.0.0"]


FROM oven/bun:1 AS builder

ARG VITE_HOSTNAME
ENV VITE_HOSTNAME=$VITE_HOSTNAME

ARG VITE_API_VERSION
ENV VITE_API_VERSION=$VITE_API_VERSION

WORKDIR /frontend

COPY ./ ./

RUN sed -i "s|PLACEHOLDER|$VITE_HOSTNAME|g" public/sitemap.xml && \
  sed -i "s|PLACEHOLDER|$VITE_HOSTNAME|g" public/robots.txt && \
  sed -i "s|PLACEHOLDER|$VITE_HOSTNAME|g" app/root.tsx

RUN bun install --frozen-lockfile
RUN bun run build

FROM nginx:1 AS production
COPY --from=builder /frontend/build/client /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
