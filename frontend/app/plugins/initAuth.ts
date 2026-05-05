export default defineNuxtPlugin(async () => {
  console.log("INIT AUTH PLUGIN");

  const { fetchUser } = useAuth();
  await fetchUser();
});