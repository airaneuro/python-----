<template>
  <div>
    <!-- 検索バー -->
    <input v-model="searchQuery" placeholder="ジャンルフィルター" />
    <select v-model="selectedGroup" @change="fetchAttributes">
      <option v-for="group in filteredGroups" :key="group">{{ group }}</option>
    </select>

    <input v-model="searchQuery2" placeholder="項目フィルター" />
    <select v-model="selectedGenre" @change="fetchAttributeDetails">
      <option v-for="attribute in filteredAttributes" :key="attribute">
        {{ attribute }}
      </option>
    </select>
    <div v-if="attributeDetails">
      <div v-for="(value, key) in attributeDetails" :key="key">
        <strong>{{ key }}:</strong> {{ value }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  async asyncData({ $axios }) {
    const groups = await $axios.$get("http://localhost:8000/api/groups");
    return { groups: groups.groups };
  },
  data() {
    return {
      genres: [],
      attributes: [],
      selectedGenre: null,
      selectedGroup: null,
      attributeDetails: null,
      searchQuery: "",
      searchQuery2: "",
    };
  },
  computed: {
    filteredGroups() {
      return this.groups.filter((group) => {
        return group.toLowerCase().includes(this.searchQuery.toLowerCase());
      });
    },
    filteredAttributes() {
      return this.attributes.filter((attribute) => {
        return attribute.toLowerCase().includes(this.searchQuery2.toLowerCase());
      });
    },
  },
  methods: {
    async fetchAttributes() {
      const { attributes } = await this.$axios.$get(
        `http://localhost:8000/api/genres/${this.selectedGroup}/attributes`
      );
      this.attributes = attributes;
    },
    async fetchAttributeDetails() {
      const { attribute_details } = await this.$axios.$get(
        `http://localhost:8000/api/attributes/${this.selectedGenre}`
      );
      this.attributeDetails = attribute_details;
    },
  },
};
</script>
