<template>
  <div>
    <b-button class="page-button shadow-none" size="sm" variant="outline"
              title="Go to First Page"
              @click="firstPage" :disabled="pageNumber==0">
              <icon name="angle-double-left"></icon>
    </b-button>
    <b-button class="page-button shadow-none" size="sm" variant="outline"
              title="Go to Previous Page"
              @click="previousPage" :disabled="pageNumber==0">
              <icon name="angle-left"></icon>
              <span class="button-text">Prev</span>
    </b-button>
    <b-dropdown aria-role="list" size="sm" variant="outline-primary"
                :text="pageNumber+1">
            <b-dropdown-item aria-role="listitem"
              v-for="page in pageCount" :key="page"
              @click="goToPage(page-1)">
              {{page}}
            </b-dropdown-item>
    </b-dropdown>
    <b-button class="page-button shadow-none" size="sm" variant="outline"
              title="Go to Next Page"
              @click="nextPage" :disabled="pageNumber >= pageCount - 1">
              <span class="button-text">Next</span>
              <icon name="angle-right"></icon>
    </b-button>
    <b-button class="page-button shadow-none" size="sm" variant="outline"
              title="Go to Last Page"
              @click="lastPage" :disabled="pageNumber >= pageCount - 1">
              <icon name="angle-double-right"></icon>
    </b-button>
  </div>
</template>

<script>
import { bus } from '../main'
export default {
  name: 'Pagination',
  props: {
    pageNumber: { type: Number, required: true },
    pageCount: { type: Number, required: true },
    needScrollTop: { type: Boolean, required: false, default: false }
  },
  methods: {
    nextPage () {
      bus.$emit('page:next')
      if (this.needScrollTop) {
        window.scrollTo(0, 0)
      }
    },
    previousPage () {
      bus.$emit('page:previous')
      if (this.needScrollTop) {
        window.scrollTo(0, 0)
      }
    },
    firstPage () {
      bus.$emit('page:first')
      if (this.needScrollTop) {
        window.scrollTo(0, 0)
      }
    },
    lastPage () {
      bus.$emit('page:last')
      if (this.needScrollTop) {
        window.scrollTo(0, 0)
      }
    },
    goToPage (page) {
      bus.$emit('page:number', page)
    }
  }
}
</script>

<style scoped lang="scss">
.page-button {
  text-align: center;
  margin: 4px 3px;
  cursor: pointer;
  outline: none;
  color: $darkblue;
  &:hover {
    color: $mainblue;
    background-color: $lightgray;
  }
  &:active {
    position:relative;
    top:1px;
  }
  &:disabled {
    color: $lightblue;
  }
}
#pageNumber {
  border-color: $lightgray;
  &:hover {
    border-color: darkgray;
  }
}
.button-text {
  margin: 10px;
}
</style>
