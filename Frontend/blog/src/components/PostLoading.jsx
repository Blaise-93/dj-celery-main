
export const PostLoadingComponent = (Component) => {

  return function PostLoadingComponent({isLoading, ...props}) {
    // if not loading  
    if(!isLoading) return <Component {...props} />
    return (
       <p>
        We are waiting for the data to load!...
       </p>
    )
  }
}
