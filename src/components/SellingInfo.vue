<template>
  <div>
    <b-card-body class="text-left">
      <h2>Your Selling Products: </h2>
      <b-card v-if="!hasSellingProducts">
        You have no products...
        <br/><br/>
        <b-button variant="outline-info" v-b-modal.productModal>Add a new product</b-button>
      </b-card>
      <b-card v-if="hasSellingProducts">
        <div class="overflow-auto">
          <b-pagination
            size="sm"
            align="center"
            v-model="currentPage"
            :total-rows="rows"
            :per-page="perPage"
          ></b-pagination>

          <b-card v-for="item in itemList" :key="item.id" no-body class="overflow-hidden"  :per-page="perPage" :current-page="currentPage">
            <b-row no-gutters>
              <b-col md="3">
                <b-img height="150px" width="150px" src="https://picsum.photos/400/400/?image=20" class="rounded-0"></b-img>
              </b-col>
              <b-col md="8">
                <b-card-body>
                  <b-card-text>
                    <b-row>
                      <b-col>Name: {{item.name}}</b-col>
                      <b-col>Brand: {{item.brand}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col>Price: ${{item.price}}</b-col>
                      <b-col>Quantity: ${{item.quantity}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col>Category: {{item.category}}</b-col>
                      <b-col>SubCategory: {{item.subCategory}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col>Description:</b-col>
                      <b-col>{{item.description}}</b-col>
                    </b-row>
                    <b-row>
                      <b-col span="2"><b-link :href="item.link">Click to see details</b-link></b-col>
                    </b-row>
                  </b-card-text>
                </b-card-body>
              </b-col>
            </b-row>
          </b-card>
        </div>
      </b-card>
    </b-card-body>

    <b-modal id="productModal" hide-footer title="Add New Product">
      <form ref="form">
        <b-row><b-col>
        <b-form-group
          :state="nameState"
          label="Name"
          label-for="name-input"
          :invalid-feedback="invalidFeedbackName"
        >
          <b-form-input
            id="name-input"
            v-model="productInput.nameInput"
            :state="nameState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col><b-col>
          <b-form-group
          :state="brandState"
          label="Brand"
          label-for="brand-input"
          :invalid-feedback="invalidFeedbackBrand"
        >
          <b-form-input
            id="Brand-input"
            v-model="productInput.brandInput"
            :state="brandState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col></b-row>
        <b-row><b-col>
        <b-form-group
          :state="categoryState"
          label="Category"
          label-for="category-input"
          :invalid-feedback="invalidFeedbackCategory"
        >
          <b-form-input
            id="category-input"
            v-model="productInput.categoryInput"
            :state="categoryState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col><b-col>
        <b-form-group
          :state="subcategoryState"
          label="Subcategory"
          label-for="subcategory-input"
          :invalid-feedback="invalidFeedbackSubcategory"
        >
          <b-form-input
            id="subcategory-input"
            v-model="productInput.subcategoryInput"
            :state="subcategoryState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col></b-row>
        <b-row><b-col>
        <b-form-group
          :state="priceState"
          label="Price"
          label-for="price-input"
          :invalid-feedback="invalidFeedbackPrice"
        >
          <b-form-input
            id="price-input"
            v-model="productInput.priceInput"
            :state="priceState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col><b-col>
        <b-form-group
          :state="quantityState"
          label="Quantity"
          label-for="quantity-input"
          :invalid-feedback="invalidFeedbackQuantity"
        >
          <b-form-input
            id="quantity-input"
            v-model="productInput.quantityInput"
            :state="quantityState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        </b-col></b-row>
        <b-form-group
          :state="discountState"
          label="Discount"
          label-for="discount-input"
          invalid-feedback="invalidFeedbackDiscount"
        >
          <b-form-input
            id="discount-input"
            v-model="productInput.discountInput"
            :state="discountState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="descriptionState"
          label="Description"
          label-for="description-input"
          invalid-feedback="invalidFeedbackDescription"
        >
          <b-form-input
            id="description-input"
            v-model="productInput.descriptionInput"
            :state="descriptionState"
            trim
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          :state="imagesState"
          label="Images"
          label-for="images-input"
          :invalid-feedback="invalidFeedbackImages"
        >
          <b-form-file
          id="images-input"
          accept=".jpg, .png, .gif"
          v-model="productInput.imagesInput"
          :state="imagesState"
          placeholder="Choose a file or drop it here..."
          drop-placeholder="Drop file here..."
          required
          ></b-form-file>
        </b-form-group>
      </form>
      <b-button type="submit" variant="outline-success" @click.prevent="addProduct" block>Add New Product</b-button>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      hasSellingProducts: false,
      perPage: 5,
      currentPage: 1,
      productInput: {
        nameInput: '',
        priceInput: '',
        categoryInput: '',
        subcategoryInput: '',
        brandInput: '',
        descriptionInput: '',
        quantityInput: '',
        discountInput: '',
        imagesInput: ''
      },
      items: [
        { name: 1, first_name: 'Fred', last_name: 'Flintstone' },
        { name: 2, first_name: 'Wilma', last_name: 'Flintstone' },
        { name: 3, first_name: 'Barney', last_name: 'Rubble' },
        { name: 4, first_name: 'Betty', last_name: 'Rubble' },
        { name: 5, first_name: 'Pebbles', last_name: 'Flintstone' },
        { name: 6, first_name: 'Bamm Bamm', last_name: 'Rubble' },
        { name: 7, first_name: 'The Great', last_name: 'Gazzoo' },
        { name: 8, first_name: 'Rockhead', last_name: 'Slate' },
        { name: 9, first_name: 'Pearl', last_name: 'Slaghoople' }
      ] // test only, to be deleted
    }
  },
  methods: { // todo add to database and to seller list
    addProduct () {
      let itemToPost = this.productInput.nameInput + ' ' + this.productInput.priceInput + ' ' + this.productInput.categoryInput + ' ' + this.productInput.subcategoryInput + ' ' + this.productInput.brandInput + ' ' + this.productInput.descriptionInput + ' ' + this.productInput.quantityInput + ' ' + this.productInput.discountInput + ' ' + this.productInput.imagesInput
      var url = 'api/resource/item?item=' + encodeURIComponent(itemToPost)
      axios
        .post(url)
        .then(response => {
          this.hasSellingProducts = true
        })
        .catch(error => alert(error))
    }
  },
  mounted: {
    getUserInfo () {
      var url = 'api/resource/sellerInfo?uid=' + encodeURIComponent(this.$store.state.uid)
      axios
        .get(url)
        .then(response => {
          this.items = response.data['offered_products']
          if (this.items.length !== 0) {
            this.hasSellingProducts = true
          }
        })
        .catch(error => alert(error))
    }
  },
  computed: {
    rows () {
      return this.items.length
    },
    itemList () {
      return this.items.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage)
    }
  }
}
</script>
