import Layout from "../components/layout";
import { getToken } from "../utils/auth";
import { fetchData } from "../utils/api";
import { useFetchUser } from "../utils/user";

function Profile({ user }) {
  const { user, loading } = useFetchUser();

  console.log("user from useFetchUser", user, loading);
  return (
    <Layout>
      <h1>Hello, {user}.</h1>
    </Layout>
  );
}

// Dashboard.getInitialProps = async ctx => {
//   const token = getToken(ctx);
//   const user = await fetchData("/api/users", token);
//   return { user };
// };

export default Profile;
