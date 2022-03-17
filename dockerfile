FROM node:16-slim as frontend
WORKDIR /app
RUN npm install -g npm

COPY package.json .
RUN npm install

COPY dsapps dsapps
RUN npm run build

CMD ["bash"]

FROM python:3.9-slim as requirements
WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
RUN python -m pip install pip --upgrade
RUN pip install wheel

COPY _requirements _requirements
COPY requirements.txt .

RUN pip install -r requirements.txt
CMD ["bash"]

FROM requirements
WORKDIR /app

ENV PORT 5000
EXPOSE 5000

COPY --from=frontend /app/dsapps dsapps
COPY dslib dslib
# COPY dsexamples dsexamples

CMD uvicorn dsapps:app --host=0.0.0.0 --port=${PORT}