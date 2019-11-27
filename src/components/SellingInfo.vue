<template>
    <div>
        <b-card-body class="text-left">
            <h2>Your Selling Products: </h2>
            <b-card v-if="!hasSellingProducts">
                You have no products...
                <br/><br/>
                <b-button variant="outline-info" @click="openModal('productModal', 0)">Add a new product</b-button>
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

                    <b-card v-for="item in itemList" :key="item.id" no-body class="overflow-hidden" :per-page="perPage"
                            :current-page="currentPage">
                        <b-row no-gutters>
                            <b-row>
                            <b-col md="3">
                                <b-img height="150px" width="150px" :src="item.images" class="rounded-0"></b-img>
                            </b-col>
                            <b-col md="7">
                                <b-card-body>
                                    <b-card-text>
                                        <b-col>
                                            <b-row>
                                                <b-link :to="'item-details/' + item.item_id">{{item.item_name}}</b-link>
                                            </b-row>
                                            <b-row>Brand: {{item.brand}}</b-row>
                                            <b-row>Price: ${{item.price}}</b-row>
                                            <b-row>Discount: {{item.discount}}</b-row>
                                            <b-row>Quantity: {{item.quantity}}</b-row>
                                            <b-row>Quantity Sold: {{item.quantity_sold}}</b-row>
                                            <b-row>Category: {{item.category}}</b-row>
                                            <b-row>SubCategory: {{item.subcategory}}</b-row>
                                            <b-row>Description:</b-row>
                                            <b-row>{{item.description}}</b-row>
                                        </b-col>
                                    </b-card-text>
                                </b-card-body>
                            </b-col>
                            </b-row>
                            <b-row align-v="center"><b-col><b-link @click="openModal('productModal', item.item_id)">Update this item</b-link></b-col></b-row>
                        </b-row>
                    </b-card>
                    <br/><br/>
                    <b-button variant="outline-info" @click="openModal('productModal', 0)">Add a new product</b-button>
                </div>
            </b-card>
        </b-card-body>

        <b-modal ref="productModal" hide-footer title="Add New Product">
            <form ref="form">
                <b-row>
                    <b-col>
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
                    </b-col>
                    <b-col>
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
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group label="Category" label-for="category-input">
                            <b-form-select id="category-input" v-model="productInput.categoryInput" required>
                                <option value="Automotives & Electronics">Automotives & Electronics</option>
                                <option value="Books">Books</option>
                                <option value="Clothing, Shoes & Accessories">Clothing, Shoes & Accessories</option>
                                <option value="Health & Beauty">Health & Beauty</option>
                                <option value="Home Supplies">Home Supplies</option>
                                <option value="Jewellery & Watches">Jewellery & Watches</option>
                            </b-form-select>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group label="Subcategory" label-for="subcategory-input">
                            <b-form-select id="subcategory-input" v-model="productInput.subcategoryInput" required>
                                <option value="Cellphones, Computers & Tablets" v-if="this.productInput.categoryInput === 'Automotives & Electronics'">Cellphones, Computers & Tablets</option>
                                <option value="Cameras & Video Games" v-if="this.productInput.categoryInput === 'Automotives & Electronics'">Cameras & Video Games</option>
                                <option value="Motos & Car Supplies" v-if="this.productInput.categoryInput === 'Automotives & Electronics'">Motos & Car Supplies</option>
                                <option value="Books" v-if="this.productInput.categoryInput === 'Books'">Books</option>
                                <option value="Women's Clothing" v-if="this.productInput.categoryInput === 'Clothing, Shoes & Accessories'">Women's Clothing</option>
                                <option value="Men's Clothing" v-if="this.productInput.categoryInput === 'Clothing, Shoes & Accessories'">Men's Clothing</option>
                                <option value="Children's Clothing" v-if="this.productInput.categoryInput === 'Clothing, Shoes & Accessories'">Children's Clothing</option>
                                <option value="Shoes" v-if="this.productInput.categoryInput === 'Clothing, Shoes & Accessories'">Shoes</option>
                                <option value="Bags & Accessories" v-if="this.productInput.categoryInput === 'Clothing, Shoes & Accessories'">Bags & Accessories</option>
                                <option value="Makeup" v-if="this.productInput.categoryInput === 'Health & Beauty'">Makeup</option>
                                <option value="Creams" v-if="this.productInput.categoryInput === 'Health & Beauty'">Creams</option>
                                <option value="Sports" v-if="this.productInput.categoryInput === 'Health & Beauty'">Sports</option>
                                <option value="Appliances" v-if="this.productInput.categoryInput === 'Home Supplies'">Appliances</option>
                                <option value="Furniture & Accessories" v-if="this.productInput.categoryInput === 'Home Supplies'">Furniture & Accessories</option>
                                <option value="Garden Supplies" v-if="this.productInput.categoryInput === 'Home Supplies'">Garden Supplies</option>
                                <option value="Pet Supplies" v-if="this.productInput.categoryInput === 'Home Supplies'">Pet Supplies</option>
                                <option value="Men's Jewellery & Watches" v-if="this.productInput.categoryInput === 'Jewellery & Watches'">Men's Jewellery & Watches</option>
                                <option value="Women's Jewellery & Watches" v-if="this.productInput.categoryInput === 'Jewellery & Watches'">Women's Jewellery & Watches</option>
                            </b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group label="Price" label-for="price-input">
                            <b-form-input
                                    id="price-input"
                                    v-model.number="productInput.priceInput"
                                    type="number" min="0.0" max="5000000.00"
                                    trim
                                    required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group label="Quantity" label-for="quantity-input">
                            <b-form-input
                                    id="quantity-input"
                                    v-model.number="productInput.quantityInput"
                                    type="number" min="1" max="1000"
                                    trim
                                    required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group label="Discount" label-for="discount-input">
                    <b-form-input
                            id="discount-input"
                            v-model.number="productInput.discountInput"
                            type="number" min="0.0" max="1.0"
                            trim
                            required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                        :state="descriptionState"
                        label="Description"
                        label-for="description-input"
                        :invalid-feedback="invalidFeedbackDescription"
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
                        label="Images"
                        label-for="images-input"
                >
                    <b-form-file
                            v-model="productInput.imageInput"
                            id="images-input"
                            accept=".jpg, .png, .gif"
                            :state="Boolean(productInput.imageInput)"
                            placeholder="Choose a file or drop it here..."
                            drop-placeholder="Drop file here..."
                            type="file"
                            required
                    ></b-form-file>
                </b-form-group>
            </form>
            <b-button type="submit" variant="outline-success" @click.prevent="addProduct" block>Add New Product
            </b-button>
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
        imageInput: null
      },
      items: [],
      focusedItemId: 0
    }
  },
  methods: {
    openModal (modal, itemId) {
      this.setFocusItemId(itemId)
      this.findModal(modal)
    },
    setFocusItemId (itemId) {
      this.focusedItemId = itemId
    },
    findModal (modal) {
      this.$refs[modal].show()
    },
    addProduct () {
      var formData = new FormData()
      formData.append('file', this.productInput.imageInput)
      let itemPayload = {item_name: this.productInput.nameInput,
        price: this.productInput.priceInput,
        category: this.productInput.categoryInput,
        subcategory: this.productInput.subcategoryInput,
        brand: this.productInput.brandInput,
        description: this.productInput.descriptionInput,
        quantity: this.productInput.quantityInput,
        discount: this.productInput.discountInput,
        images: this.productInput.imageInput.name}
      formData.append('item', JSON.stringify(itemPayload))
      if (this.focusedItemId === 0) {
        var url = 'api/resource/item'
        axios
          .post(url, formData, {headers: {'Content-Type': 'multipart/form-data'}})
          .then(response => {
            this.getSellingProducts()
            this.$refs['productModal'].hide()
          })
          .catch(error => alert(error))
      } else {
        url = 'api/resource/item/' + this.focusedItemId
        axios
          .put(url, formData, {headers: {'Content-Type': 'multipart/form-data'}})
          .then(response => {
            this.getSellingProducts()
            this.$refs['productModal'].hide()
          })
          .catch(error => alert(error))
      }
    },
    getSellingProducts () {
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
  mounted () {
    this.getSellingProducts()
  },
  computed: {
    rows () {
      return this.items.length
    },
    itemList () {
      return this.items.slice((this.currentPage - 1) * this.perPage, this.currentPage * this.perPage)
    },
    nameState () {
      if (this.productInput.nameInput.match(/^[A-Za-z\s\d*&()]{1,300}$/)) {
        return true
      } else if (this.productInput.nameInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackName () {
      if (this.productInput.nameInput.match(/^[A-Za-z\s\d*&()]{1,300}$/) || this.productInput.nameInput === '') {
        return ''
      } else {
        return 'Please enter a valid product name'
      }
    },
    brandState () {
      if (this.productInput.nameInput.match(/^[A-Za-z\s\d*&()@]{1,120}$/)) {
        return true
      } else if (this.productInput.nameInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackBrand () {
      if (this.productInput.nameInput.match(/^[A-Za-z\s\d*&()@]{1,120}$/) || this.productInput.nameInput === '') {
        return ''
      } else {
        return 'Please enter a valid brand name'
      }
    },
    descriptionState () {
      if (this.productInput.nameInput.match(/^[A-Za-z\s*&()#!?%_]{1,1000}$/)) {
        return true
      } else if (this.productInput.nameInput === '') {
        return null
      } else {
        return false
      }
    },
    invalidFeedbackDescription () {
      if (this.productInput.nameInput.match(/^[A-Za-z\s*&()#!?%_]{1,1000}$/) || this.productInput.nameInput === '') {
        return ''
      } else {
        return 'Please enter a valid description'
      }
    }
  }
}
</script>
