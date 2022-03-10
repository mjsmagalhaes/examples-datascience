FROM node:16-slim as frontend

COPY dsapps app/dsapps

WORKDIR /app/dsapps/wordcloud/templates
RUN npm install
RUN npx parcel build --public-url /wordcloud/assets
RUN rm -rf node_modules
CMD ["bash"]

FROM python:3.9-slim as backend
WORKDIR /app

COPY _requirements _requirements
COPY requirements.txt requirements.txt
COPY --from=frontend /app/dsapps dsapps
COPY dslib dslib
# COPY dsexamples dsexamples

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN python -m pip install pip --upgrade
RUN pip install wheel
RUN pip install -r requirements.txt

ENV PORT 5000
EXPOSE 5000

CMD uvicorn dsapps:app --host=0.0.0.0 --port=${PORT}