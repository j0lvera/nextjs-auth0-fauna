import React from "react";
import nookies from "nookies";

/**
 * Return token from cookies if it's present, otherwise redirects user to
 * authentication endpoint (login/signup)
 *
 * @param {string} ctx Next's ctx
 * @returns {string}
 */
function getToken(ctx) {
  const { token } = nookies.get(ctx);

  if (ctx.req && !token) {
    ctx.res.writeHead(302, { Location: "/api/auth" });
    ctx.res.end();
    return;
  }

  return token;
}

const withAuth = WrappedComponent => {
  const Wrapper = props => <WrappedComponent {...props} />;
  Wrapper.getInitialProps = async ctx => {
    const componentProps =
      WrappedComponent.getInitialProps &&
      (await WrappedComponent.getInitialProps(ctx));

    if (typeof window === "undefined") {
      const token = getToken(ctx);

      return { ...componentProps, token };
    }
    return { ...componentProps };
  };

  return Wrapper;
};

export { getToken, withAuth };
