import jwtDecode from "jwt-decode";
import nookies from "nookies";
import axios from "axios";

function getToken(ctx) {
  const { token } = nookies.get(ctx);

  if (ctx.req && !token) {
    ctx.res.writeHead(302, { Location: "/api/auth" });
    ctx.res.end();
    return;
  }

  return token;
}

async function fetchUser(token = "") {
  const isClient = typeof window !== "undefined";

  if (isClient && window.__user) {
    return window.__user;
  }

  const headers = token ? { headers: { Cookie: `token=${token}` } } : {};
  const options = Object.assign({}, { withCredentials: true }, headers);

  console.log("options", options);

  try {
    const { data, status } = await axios(
      `${process.env.APP_URL}/api/users`,
      options
    );

    console.log("response", data);

    if (status !== 200) {
      delete window.__user;
      return null;
    }

    const json = data.message.user;
    if (isClient) {
      window.__user = json;
    }
    return json;
  } catch (error) {
    // console.log("error while trying fetchUser", error.response);
  }
}

const withAuth = WrappedComponent => {
  const Wrapper = props => <WrappedComponent {...props} />;
  Wrapper.getInitialProps = async ctx => {
    const componentProps =
      WrappedComponent.getInitialProps &&
      (await WrappedComponent.getInitialProps(ctx));

    if (typeof window === "undefined") {
      const token = getToken(ctx);
      const user = jwtDecode(token);

      return { ...componentProps, user };
    }
    return { ...componentProps };
  };

  return Wrapper;
};

export { getToken, withAuth, fetchUser };
