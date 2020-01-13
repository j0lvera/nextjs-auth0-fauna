import { useState, useEffect } from "react";
import { fetchData } from "./api";

// Code mostly stolen from
// https://github.com/zeit/next.js/blob/canary/examples/auth0/lib/user.js

async function fetchUser() {
  const isClient = typeof window !== "undefined";

  if (isClient && window.__user) {
    return window.__user;
  }

  try {
    const { data } = await fetchData({}, "/api/users");

    if (isClient) {
      window.__user = data;
    }

    return data;
  } catch (error) {
    if (error.response) {
      const { status } = error.response;

      if (isClient && status === 401) {
        delete window.__user;
        location.href = `${process.env.APP_URL}/api/auth`;
        return;
      }
    }

    console.log("Something went wrong when fetchUser", error);
    delete window.__user;
    return null;
  }
}

function useFetchUser({ required } = {}) {
  const isClient = typeof window !== "undefined";

  const [loading, setLoading] = useState(() => !(isClient && window.__user));
  const [user, setUser] = useState(() => (isClient && window.__user) || null);

  useEffect(() => {
    if (!loading && user) {
      return;
    }

    setLoading(true);
    let isMounted = true;

    fetchUser().then(user => {
      // Only set the user if the component is still mounted
      if (isMounted) {
        // When the user is not logged in but login is required
        if (required && !user) {
          window.location.href = "/api/auth";
          return;
        }
        setUser(user);
        setLoading(false);
      }
    });

    return () => {
      isMounted = false;
    };
  }, []);

  return { user, loading };
}

export { fetchUser, useFetchUser };
