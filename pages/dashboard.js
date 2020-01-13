import Layout from "../components/layout";
import { getToken } from "../utils/auth";
import { fetchData } from "../utils/api";

function Dashboard({ user }) {
  return (
    <Layout>
      <h1>Hello, {user}.</h1>

      <p>
        We load data from the server on this page using{" "}
        <code>getInitialProps</code>.
      </p>
    </Layout>
  );
}

Dashboard.getInitialProps = async ctx => {
  const token = getToken(ctx);
  console.log("token from Next.js getInitialProps", token);

  const { data } = await fetchData(ctx, "/api/users", token);
  console.log("user object from Next.js getInitialProps", data);

  return { user: data.user };
};

export default Dashboard;
