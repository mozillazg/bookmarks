<template>
  <section class="section content">
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
            <td v-if="bookmark.starred">🌟</td>
            <td v-else></td>
            <td><a :href=bookmark.url >{{ bookmark.title }}</a></td>
            <td>
              <span v-for="tag in bookmark.tags">
                <router-link :to="{name: 'urls', query: {tag: tag.name} }"
                 class="tag is-info">{{ tag.name }}</router-link>&nbsp;
              </span>
            </td>
            <td>
              <span v-for="category in bookmark.categories">
                <router-link :to="{name: 'urls', query: {category: category.name} }"
                 class="tag is-info">{{ category.name }}</router-link>&nbsp;
              </span>
            </td>
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
