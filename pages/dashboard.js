import Layout from "../components/layout";
import { getToken, fetchUser } from "../utils/auth";

function Dashboard({ user }) {
  return (
    <Layout>
      <div>Hello, {user}.</div>
    </Layout>
  );
}

Dashboard.getInitialProps = async ctx => {
  const token = getToken(ctx);

  const user = await fetchUser(token);

  return { user };
};

export default Dashboard;
