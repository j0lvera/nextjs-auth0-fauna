# Authentication example with Next.js, Auth0 and FaunaDB

Small web application built with Next.js that uses Auth0 for Authentication, FaunaDB as database and ZEIT Now for hosting. The API is built with [Python Serverless Functions](https://zeit.co/docs/runtimes#official-runtimes/python) that use Bottle to handle requests.

## Getting started

The example uses the the API-frontend architecture that [ZEIT recommends](https://github.com/zeit/now-examples/tree/master/gatsby-functions). Our Python functions inside an `api/` folder and our Next.js frontend in the root folder.

### Prerequisites

#### System requirements

- [Python](https://www.python.org) v3.6.0 or later
- [Poetry](https://python-poetry.org/) v0.12.17
- [Node.js](https://nodejs.org/) v8.x or later
- [npm](https://www.npmjs.com/) v6.x or later
- [git](https://git-scm.com/) v2.14.1 or later
- [now](https://github.com/zeit/now) v16.x or later

#### FaunaDB setup

- [Create a FaunaDB account](https://dashboard.fauna.com).
- Create a database for this example.
  - Click the New Database button,
  - enter "auth0-fauna", and
  - click Save.
- Create a new collection and enter "users" as name.
- Create a new index, enter "users_by_auth0_id" with these settings:
  - Source Collection: "users",
  - Index Name: "users_by_auth0_id",
  - Terms: "data.auth0UserId",
  - Values: Leave it empty,
  - Unique: Checked,
  - Serialized: Checked,
- Create a server key.
  - Click Security in the left navigation bar,
  - Click New Key,
  - select "auth0-fauna" in the Database field,
  - set role as "Admin", and
  - click Save.

#### Auth0 setup

- [Create an Auth0 Account](https://auth0.com/)
- Create an application for this example.
  - Click Create Application,
  - Select "Regular Web Applications",
  - Click in the "Settings" tab and
  - Copy the Domain, Client ID and Client Secret.

#### ~~Post-User-registration hook (Optional)~~

~~In case we want to keep a copy of the user data in our database, we need to setup a [Post-User-Registration hook in Auth0](https://auth0.com/docs/hooks/guides/use-the-post-user-registration-extensibility-point). The hook will send a POST request to our API with the Auth0's `userId`. Then, we save the information in our database in case we need to build relations with other tables.~~

#### Ngrok setup

[Install ngrok the instructions from their website](https://ngrok.com/product). We will use ngrok to expose our local server so that Auth0 can reach it with a [Hook](https://auth0.com/docs/hooks) we will setup.

Run ngrok in our port 3000.

```
ngrok http 3000
```

### Installing

Clone the repository.

```
$ git clone https://github.com/j0lv3r4/nextjs-auth0-fauna.git
```

Copy the `.env.example` file into `.env` for our Serverless Functions and `.env.build` for our Next.js build.

Fill the values in both `.env` and `.env.build` files with the following:

- The FaunaDB server key.
- The Auth0 Client ID, Client Secret and Auth0 domain.
- The URL that ngrok gives us. Keep in mind that ngrok will give us a new URL every time we use start it.

Your files should look like below.

```
SECRET=a secret!
SALT=salty
FAUNADB_SERVER_KEY=YMyGXF2PGfRl0sSS7-fnADhxWfvIACEmmZUpRdD29q4bWLq4UP
AUTH0_CLIENT_ID=tuXA7ldwyrCNCXC8tuXA7ldwyrCNCXC8
AUTH0_CLIENT_SECRET=x5qjKZdW-ffiQjLeY7x5qjKZdW-ffiQjLeY7
AUTH0_DOMAIN=https://babyyoda.auth0.com
APP_URL=https://random-url.ngrok.io
DEBUG=True
```

In the root directory of the project, we install our npm dependencies.

```
$ cd nextjs-auth0-fauna
$ npm install
```

In the `api/` folder, install the Python dependencies.

```
$ cd api
$ poetry install
```

### Start the development server

Inside the root project folder we run our local server.

```
$ now dev
```
