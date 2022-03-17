FROM node:16-slim as frontend
WORKDIR /app
COPY package.json .
COPY dsapps dsapps

RUN npm install -g npm
RUN npm install
RUN npm run build
CMD ["bash"]

FROM python:3.9-slim as requirements
WORKDIR /app

COPY _requirements _requirements
COPY requirements.txt requirements.txt

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN python -m pip install pip --upgrade
RUN pip install wheel
RUN pip install -r requirements.txt
CMD ["bash"]

FROM requirements
WORKDIR /app

COPY --from=frontend /app/dsapps dsapps
COPY dslib dslib
# COPY dsexamples dsexamples

ENV PORT 5000
EXPOSE 5000

CMD uvicorn dsapps:app --host=0.0.0.0 --port=${PORT}