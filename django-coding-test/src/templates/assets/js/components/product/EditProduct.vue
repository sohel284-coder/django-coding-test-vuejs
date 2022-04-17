<template>
  <section>
     <head>Hello</head>
    <button type="submit" class="btn btn-lg btn-primary">
      
    </button>
    <button type="button" class="btn btn-secondary btn-lg">Cancel</button>
  </section>
</template>

<script>
import vue2Dropzone from "vue2-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";
import InputTag from "vue-input-tag";
import axios from "axios";

export default {
  components: {
    vueDropzone: vue2Dropzone,
    InputTag,
  },
  props: {
    slug: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      product_name: "",
      product_sku: "",
      description: "",
      images: [],
      product_slug:this.slug,
     
      product_variant_prices: [],
      dropzoneOptions: {
        url: "https://httpbin.org/post",
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        headers: { "My-Awesome-Header": "header value" },
      },
    };
  },
  methods: {

  },
  created:function(){
      console.log(this.product_slug);
  },
};
</script>