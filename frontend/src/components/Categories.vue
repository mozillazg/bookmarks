<template>
  <section class="section">
    <div class="container">
      <span v-for="category in categories">
        <router-link :to="{name: 'urls', query: {category: category.name} }"
          class="tag is-info">{{ category.name }}({{ category.url_number }})</router-link>&nbsp;
      </span>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Categories',
  data: function () {
    return {
      categories: []
    }
  },
  created: function () {
    this.fetchData()
  },
  methods: {
    fetchData: function () {
      this.fetch()
    },
    fetch: function () {
      const url = '/api/v1/categories'
      this.$http.get(url).then((response) => {
        this.categories = response.body
      })
    }
  }
}
</script>
