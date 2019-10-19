<template>
  <div>
    <b-button class="page-button" type="is-link" title="Go to First Page"
    @click="firstPage" :disabled="pageNumber==0"
    icon-left="angle-double-left icon-color">
    </b-button>
    <b-button class="page-button" type="is-link" title="Go to Previous Page"
              @click="previousPage" :disabled="pageNumber==0"
              icon-left="angle-left icon-color">
              Prev
    </b-button>
    <b-dropdown aria-role="list">
            <b-button id="pageNumber" class="page-button" type="is-link" title="Go to Page #" slot="trigger"
              icon-right="angle-down icon-color">
              <span>{{pageNumber+1}}</span><br>
            </b-button>
            <b-dropdown-item aria-role="listitem"
              v-for="page in pageCount" :key="page"
              @click="goToPage(page-1)">
              {{page}}
            </b-dropdown-item>
    </b-dropdown>
    <b-button class="page-button" type="is-link" title="Go to Next Page"
              @click="nextPage" :disabled="pageNumber >= pageCount - 1"
              icon-right="angle-right icon-color">
              Next
    </b-button>
    <b-button class="page-button" type="is-link" title="Go to Last Page"
              @click="lastPage" :disabled="pageNumber >= pageCount - 1"
              icon-right="angle-double-right icon-color">
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
      if (this.needScrollTop) {
        window.scrollTo(0, 0)
      }
    }
  }
}
</script>

<style scoped lang="scss">
.page-button {
  border-color: transparent;
  size: "is-size-6";
  text-align: center;
  margin: 4px 3px;
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
#pageNumber {
  border-color: $lightgray;
  &:hover {
    border-color: darkgray;
  }
}
</style>
