FROM apify/actor-node:20
USER root

# 패키지 설치
COPY package*.json ./
RUN npm ci

# 소스 복사 및 빌드
COPY . ./
RUN npm run build

# 엔트리포인트
CMD ["node", "dist/index.js"]
