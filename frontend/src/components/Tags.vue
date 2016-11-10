<template>
  <section class="section">
    <div class="container">
      <span v-for="tag in tags">
        <router-link :to="{name: 'urls', query: {tag: tag.name} }"
          class="tag is-info">{{ tag.name }}({{ tag.url_number }})</router-link>&nbsp;
      </span>
    </div>
  </section>
</template>

<script>
export default {
  name: 'Tags',
  data: function () {
    return {
      tags: []
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
      const url = '/api/v1/tags'
      this.$http.get(url).then((response) => {
        this.tags = response.body
      })
    }
  }
}
</script>
