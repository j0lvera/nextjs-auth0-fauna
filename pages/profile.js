import Layout from "../components/layout";
import { useFetchUser } from "../utils/user";

function Profile() {
  const { user, loading } = useFetchUser();

  return (
    <Layout user={user.user} loading={loading}>
      {loading ? "loading..." : <h1>Hello, {user.user}.</h1>}
      <p>We load data from the client on this page.</p>
    </Layout>
  );
}

export default Profile;
