import Layout from "../components/layout";
import { getToken, fetchUser } from "../utils/auth";

function Dashboard({ user }) {
  return (
    <Layout>
      <h1>Hello, {user}.</h1>
    </Layout>
  );
}

Dashboard.getInitialProps = async ctx => {
  const token = getToken(ctx);
  const user = await fetchUser(token);
  return { user };
};

export default Dashboard;
