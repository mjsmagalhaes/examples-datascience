FROM node:16-slim as frontend

COPY . app

WORKDIR /app/dsapps/wordcloud/templates
RUN npm install
RUN npx parcel build --public-url /wordcloud/assets
RUN rm -rf node_modules

FROM python:3.9-slim as backend

COPY . app
COPY --from=frontend /app/dsapps /app/dsapps

WORKDIR /app
RUN python -m venv .venv
ENV PATH="/app/.venv/bin:$PATH"
RUN python -m pip install pip --upgrade
RUN pip install -r requirements.txt

ENV PORT 5000
EXPOSE 5000

CMD uvicorn dsapps:app --host=0.0.0.0 --port=${PORT}