FROM oven/bun:1 AS development

WORKDIR /frontend

COPY ./ ./
RUN bun install --frozen-lockfile
CMD [ "bun", "run", "dev", "--host", "0.0.0.0"]





FROM oven/bun:1 AS production

WORKDIR /frontend

COPY ./ ./
RUN bun install --frozen-lockfile --production
RUN bun run test && bun run build

FROM nginx:1
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=production /frontend/build/client /usr/share/nginx/html
