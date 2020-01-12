import NextHead from "next/head";
import Link from "next/link";

function Layout({ children }) {
  return (
    <>
      <header>
        <NextHead>
          <meta charSet="UTF-8" />
          <title>
            Authentication example with Fauna, Auth0, Python and Next.js
          </title>

          <meta name="viewport" content="width=device-width, initial-scale=1" />
        </NextHead>

        <nav>
          <ul>
            <li>
              <Link href="/">
                <a>Home</a>
              </Link>
            </li>
            <li>
              <Link href="/api/auth">
                <a>Login</a>
              </Link>
            </li>
            <li>
              <Link href="/dashboard">
                <a>Dashboard</a>
              </Link>
            </li>
            <li>
              <Link href="/api/logout">
                <a>Logout</a>
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      <main>{children}</main>

      <footer>
        Example by <a href="https://twitter.com/_jolvera">@_jolvera</a>
      </footer>
    </>
  );
}

export default Layout;
