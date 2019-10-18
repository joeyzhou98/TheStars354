<template>
  <div>
    <b-button class="category-button" type="is-link"
              icon-left="bars icon-color"
              @click="openMenu">
              SHOP
    </b-button>
    <Slide noOverlay :isOpen="this.open" @closeMenu="closeMenu">
      <a id="home" href="#">
        <span>Home</span>
      </a>
    </Slide>
  </div>
</template>>

<script>
// vue-burger-menu source and help:
// https://vuejsexamples.com/an-off-canvas-sidebar-vue-component/
// https://github.com/mbj36/vue-burger-menu/wiki/FAQ

import { Slide } from 'vue-burger-menu'

export default {
  name: 'CategoriesMenu',
  components: {
    Slide
  },
  data () {
    return {
      open: false
    }
  },
  methods: {
    openMenu () {
      this.open = true
    },
    closeMenu () {
      this.open = false
    }
  }
}
</script>

<style scoped lang="scss">
.category-button {
  text-align: center;
  cursor: pointer;
  outline: none;
  color: $darkblue;
  &:hover {
    color: $mainblue;
  }
  &:active {
    position:relative;
    top:1px;
  }
}
</style>

<style lang="scss"> // Unscoped section! These classes are defined in the Slide component
Slide {
  width: 250px;
}
.bm-burger-button {
  display: none;
}
.bm-burger-bars {
  background-color:$darkgray;
}
.line-style {
  position: absolute;
  height: 20%;
  left: 0;
  right: 0;
}
.cross-style {
  position: absolute;
  top: 12px;
  right: 2px;
  cursor: pointer;
}
.bm-cross {
  background: #bdc3c7;
}
.bm-cross-button {
  height: 24px;
  width: 24px;
}
.bm-menu {
  height: 100%; /* 100% Full-height */
  width: 0; /* 0 width - change this with JavaScript */
  position: fixed; /* Stay in place */
  z-index: 1000; /* Stay on top */
  top: 0;
  left: 0;
  background-color: $darkblue;
  overflow-x: hidden; /* Disable horizontal scroll */
  padding-top: 60px; /* Place content 60px from the top */
  transition: 0.5s; /*0.5 second transition effect to slide in the sidenav*/
}
.bm-item-list {
  color: #b8b7ad;
  margin-left: 10%;
  font-size: 20px;
}
.bm-item-list > * {
  display: flex;
  text-decoration: none;
  padding: 0.7em;
}
.bm-item-list > * > span {
  margin-left: 10px;
  font-weight: 700;
  color: white;
}
</style>
