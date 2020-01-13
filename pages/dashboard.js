import Layout from "../components/layout";
import { getToken } from "../utils/auth";
import { fetchData } from "../utils/api";

function Dashboard({ user }) {
  return (
    <Layout>
      <h1>Hello, {user}.</h1>
    </Layout>
  );
}

Dashboard.getInitialProps = async ctx => {
  const token = getToken(ctx);
  console.log("token from Next.js getInitialProps", token);

  const { data } = await fetchData(ctx, "/api/users", token);
  console.log("user from Next.js getInitialProps", data);

  return { user: data.user };
};

export default Dashboard;
