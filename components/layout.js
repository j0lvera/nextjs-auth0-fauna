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
          <Link href="/api/auth">
            <a>Login</a>
          </Link>
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
