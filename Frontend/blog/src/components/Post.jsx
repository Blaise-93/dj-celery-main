export const Post = (props) => {
  const { posts } = props;
  console.log(posts);
  if (!posts || posts.length === 0) return <p>Cannot find any posts, sorry</p>;

  return (
    <div className="post-container">
      {posts.map((post) => {
        return (
          <div className="post" key={post.id}>
                <p>{post.title}</p>
                <p>{post.category}</p>
                <p>{post.content.substr(0, 50)}</p>
                <p>{post.excerpt.substr(0, 50)}</p>
                <p>{post.published}</p>
                <p>{post.status}</p>
              
          </div>
        );
      })}
    </div>
  );
};
