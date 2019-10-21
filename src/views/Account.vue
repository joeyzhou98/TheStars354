<template>
  <div>
    <b-card
    title="Welcome XXX"
    img-src="https://picsum.photos/600/300/?image=25"
    img-alt="Image"
    img-top
    tag="article"
    style="width: 60rem; display: inline-block;"
    class="mb-2"
  >
    <b-card-text>
      You can change your personal details, manage your orders, and much more.
    </b-card-text>

    <b-nav tabs justified>
      <b-nav-item active href="#/login/">PROFILE</b-nav-item>
      <b-nav-item active href="#/login/">ORDER HISTORY</b-nav-item>
      <b-nav-item active href="#/login/">XXXXXX</b-nav-item>
      <b-nav-item active href="#/login/">XXXXXX</b-nav-item>
    </b-nav>
    <br/>
    <b-button type="submit" variant="dark" href="#/">Logout</b-button>
    </b-card>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped lang="scss">

</style>
