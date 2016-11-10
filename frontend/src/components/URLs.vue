<template>
  <section class="section">
    <div class="container">
      <table class="table">
        <thead>
          <tr>
            <th>Starred</th>
            <th>Title</th>
            <th>Tags</th>
            <th>Categories</th>
            <th>Note</th>
            <th>Updated</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="bookmark in urls">
            <td>{{ bookmark.starred }}</td>
            <td><a :href=bookmark.url >{{ bookmark.title }}</a></td>
            <td>{{ bookmark.tags }}</td>
            <td>{{ bookmark.categories }}</td>
            <td>{{ bookmark.note }}</td>
            <td>{{ bookmark.updated_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script>
export default {
  name: 'URLs',
  data: function () {
    return {
      urls: []
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
      const url = '/api/v1/urls'
      this.$http.get(url).then((response) => {
        this.urls = response.body
      })
    }
  }
}
</script>
