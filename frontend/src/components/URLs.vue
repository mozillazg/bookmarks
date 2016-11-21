<template>
  <section class="section content">
    <div class="container">
      <form v-on:submit.prevent="submitSearch">
        <p class="control has-addons has-addons-centered">
          <input class="input" type="text" placeholder="Amount of money"
           v-model="search">
          <a class="button is-primary"
           v-on:click.prevent="submitSearch">
            Search
          </a>
        </p>
      </form>

      <nav class="pagination">
        <router-link :to="routeLink('prePage')" class="button">Previous</router-link>
        <router-link :to="routeLink('nextPage')" class="button">Next page</router-link>
        <ul></ul>
      </nav>

      <table class="table is-bordered is-striped is-narrow">
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
            <td><a :href="'/admin/url/edit/?url=%2Fadmin%2Furl%2F&id=' + bookmark.id ">{{ bookmark.updated_at }}</a></td>
          </tr>
        </tbody>
      </table>

      <nav class="pagination">
        <router-link :to="routeLink('prePage')" class="button">Previous</router-link>
        <router-link :to="routeLink('nextPage')" class="button">Next page</router-link>
        <ul></ul>
      </nav>
    </div>
  </section>
</template>

<script>
import pageMixin from '../mixins/page'

export default {
  name: 'URLs',
  mixins: [pageMixin],
  data: function () {
    return {
      urls: [],
      page: 1,
      tag: this.$route.query.tag || '',
      category: this.$route.query.category || '',
      search: this.$route.query.search || ''
    }
  },
  created: function () {
    this.fetchData()
  },
  watch: {
    '$route': 'fetchData'
  },
  methods: {
    fetchData: function () {
      this.fetch()
    },
    fetch: function () {
      const query = this.getQueryParams()
      const url = '/api/v1/urls'
      this.$http.get(url, {params: query}).then((response) => {
        this.urls = response.body
      })
    },
    routeLink: function (action) {
      var query = this.getQueryParams()
      if (action === 'nextPage') {
        query.page = this.nextPage()
        return {name: 'queueErrors', query: query}
      } else if (action === 'prePage') {
        query.page = this.prePage()
        return {name: 'queueErrors', query: query}
      }
    },
    getQueryParams: function () {
      return {
        page: this.currentPage(),
        tag: this.tag,
        category: this.category,
        search: this.search
      }
    },
    submitSearch: function () {
      this.$router.push({name: 'urls', query: this.getQueryParams()})
    }
  }
}
</script>
