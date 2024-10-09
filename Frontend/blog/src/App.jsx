import "./App.css";
import { useEffect, useState } from "react";
import { PostLoadingComponent } from "./components/PostLoading";
import { Post } from "./components/Post";

function App() {
  const [appState, setAppState] = useState({ isLoading: true, posts: null });

  const PostLoading = PostLoadingComponent(Post);

  useEffect(() => {
    const url = "http://127.0.0.1:8000/api";

    setAppState({ isLoading: true });
    fetch(url).then(res => res.json()
        .then(posts =>  {
          setAppState({isLoading:false, posts:posts})
        })
  );
      
  }, []);

  return (
    <div className="app-container">
        <h1 className="post-info">Latest Posts</h1>
        <PostLoading isLoading={appState.isLoading} posts={appState.posts}/>
    </div>
  )

}

export default App;
