import axios from "axios";
import nookies from "nookies";

const api = axios.create({
  baseURL: `${process.env.APP_URL}`,
  withCredentials: true
});

async function fetchData(ctx, endpoint = "/", token = "") {
  const isClient = typeof window !== "undefined";

  const headers = token ? { headers: { Cookie: `token=${token}` } } : {};
  const reqOptions = Object.assign({}, { withCredentials: true }, headers);

  try {
    const { data } = await api.get(endpoint, reqOptions);
    console.log('data', data);
    return { data };
  } catch (error) {
    console.log("Error while trying to fetch data", error);
    // Always destroy the cookie on error.
    nookies.destroy(ctx, "token");

    if (!isClient && error.response) {
      const { status } = error.response;

      if (status === 401) {
        ctx.res.writeHead(302, { Location: "/api/auth" });
        ctx.res.end();
        return;
      }
    }
  }
}

export { fetchData };
