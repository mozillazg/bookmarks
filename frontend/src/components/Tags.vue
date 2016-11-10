<template>
  <section class="section">
    <div class="container">
      <span v-for="tag in tags">
        <span class="tag is-info">{{ tag.name }}</span>
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
