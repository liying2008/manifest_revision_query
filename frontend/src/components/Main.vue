<template>
  <div id="main-container">
    <el-header>
      <el-row class="autocomplete"
              gutter="40">
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            v-model="project"
            :fetch-suggestions="queryProject"
            placeholder="输入 Project 名称"
            @keyup.enter.native="search"
            @select="handleSelect">
            <template slot="prepend">Project</template>
          </el-autocomplete>
        </el-col>
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            v-model="manifest"
            :fetch-suggestions="queryManifest"
            placeholder="输入 Manifest 文件名"
            @keyup.enter.native="search"
            @select="handleSelect">
            <template slot="prepend">Manifest File</template>
          </el-autocomplete>
        </el-col>
        <el-col :span="4">
          <el-button class="inline-button"
                     @click="search">搜索
          </el-button>
        </el-col>
      </el-row>

    </el-header>
    <el-container>
      <el-table
        :data="tableData"
        height="800"
        align="left"
        border
        highlight-current-row
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index">
        </el-table-column>
        <el-table-column
          prop="manifest"
          header-align="center"
          label="Manifest File"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="project"
          header-align="center"
          label="Project"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="path"
          header-align="center"
          label="Path"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="revision"
          header-align="center"
          label="Revision"
          width="'25%'">
        </el-table-column>
      </el-table>
    </el-container>
  </div>
</template>

<script>
  export default {
    name: 'Main',

    data() {
      return {
        SEPARATOR: '@@',
        project: '',
        manifest: '',
        projects: [],
        manifests: [],
        tableData: []
      }
    },
    methods: {
      queryProject(queryString, cb) {
        var projects = this.projects;
        var results = queryString ? projects.filter(this.createFilter(queryString)) : projects;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      queryManifest(queryString, cb) {
        var manifests = this.manifests;
        var results = queryString ? manifests.filter(this.createFilter(queryString)) : manifests;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) >= 0);
        };
      },
      handleSelect(item) {
        console.log(item);
      },
      loadDataFromManifest(filterProject) {
        let manifest = this.manifest.replace(/\//g, this.SEPARATOR).trim();
        this.$axios.get('/static/manifests/' + manifest).then((res) => {
          // console.log(res.data)
          if (!filterProject) {
            this.tableData = res.data
          } else {
            this.tableData = res.data.filter((val) => {
              return val.project === this.project
            });
            if (this.tableData.length === 0) {
              this.$message.error('没有匹配项：' + this.manifest + ' 和 ' + this.project);
            }
          }
        }).catch(error => {
          console.log(error);
          this.tableData = [];
          this.$message.error('未找到 Manifest 文件：' + this.manifest);
        });
      },

      loadDataFromProject() {
        let project = this.project.replace(/\//g, this.SEPARATOR, -1).trim();
        console.log(project)
        this.$axios.get('/static/projects/' + project).then((res) => {
          // console.log(res.data)
          this.tableData = res.data
        }).catch(error => {
          console.log(error);
          this.tableData = [];
          this.$message.error('未找到 Project：' + this.project);
        });
      },

      search() {
        this.project = this.project.trim();
        this.manifest = this.manifest.trim();
        if (this.project === '' && this.manifest === '') {
          this.$message.error('仓库 和 Manifest 文件 需要至少填写一项');
        } else if (this.project === '') {
          // manifest 有值
          this.loadDataFromManifest(false)
        } else if (this.manifest === '') {
          // project 有值
          this.loadDataFromProject()
        } else {
          // project 和 manifest 都有值
          this.loadDataFromManifest(true)
        }
      }
    },
    mounted() {
      this.$axios.get('/static/projects.list').then((res) => {
        let projects = res.data.split('\n');
        this.projects = projects.map(project => {
          let obj = {};
          obj.value = project;
          return obj
        });
      });
      this.$axios.get('/static/manifests.list').then((res) => {
        let manifests = res.data.split('\n');
        this.manifests = manifests.map(manifest => {
          let obj = {};
          obj["value"] = manifest;
          return obj
        });
      })
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #main-container {
    margin: 20px 26px 26px 20px;
  }

  #main-container .el-header {
    padding: 0;
  }

  #main-container .inline-input {
    width: 100%;
    margin-right: 10px;
  }

  #main-container .inline-button {
    width: 100%;
  }

</style>
