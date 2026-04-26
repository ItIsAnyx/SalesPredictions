FROM node:22 AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build

FROM node:22-slim
WORKDIR /app

COPY --from=build /app/.output/ ./.output

ENV PORT=3000
ENV NODE_ENV=production

CMD ["node", ".output/server/index.mjs"]