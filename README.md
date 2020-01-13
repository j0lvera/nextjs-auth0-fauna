# Authentication example with Auth0 and Fauna

On the frontend, the session is valid as long as the cookie is present. When we try to send a request to the server, the backend will validate the token and if it's invalid it will expire the token in Fauna and delete the cookie in the response.

## Avoiding multiple requests to get user's info.

Having user's info handy is a common pattern in any web app.

An object in the global `window` keeps our data available and avoids unnecesary calls to the server. The backend will validate the token when we need to perform an action anyway.
