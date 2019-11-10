<template>
  <div id="main-container">
    <el-header>
      <el-row class="autocomplete"
              :gutter="40">
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            clearable
            v-model="project"
            ref="input_project"
            :fetch-suggestions="queryProject"
            :placeholder="projectInputPlaceholder"
            @select="handleSelect">
            <el-select v-model="projectSelect" slot="prepend" :value="projectSelect">
              <el-option label="Project" value="project"></el-option>
              <el-option label="Path" value="path"></el-option>
            </el-select>
          </el-autocomplete>
        </el-col>
        <el-col :span="10">
          <el-autocomplete
            class="inline-input"
            clearable
            v-model="manifest"
            ref="input_manifest"
            :fetch-suggestions="queryManifest"
            :placeholder="manifestInputPlaceholder"
            @select="handleSelect">
            <el-select v-model="manifestSelect" slot="prepend" :value="manifestSelect">
              <el-option label="Manifest" value="manifest"></el-option>
              <el-option label="Revision" value="revision"></el-option>
            </el-select>
          </el-autocomplete>
        </el-col>
        <el-col :span="4">
          <el-button class="inline-button"
                     icon="el-icon-search"
                     @click="search">Search
          </el-button>
        </el-col>
      </el-row>

    </el-header>
    <el-container>
      <el-table
        :data="tableData"
        :height="tableHeight"
        v-loading="loading"
        align="left"
        border
        ref="main_table"
        @cell-dblclick="cellDoubleClick"
        highlight-current-row
        style="width: 100%">
        <el-table-column
          header-align="center"
          type="index">
        </el-table-column>
        <el-table-column
          prop="manifest"
          sortable
          header-align="center"
          label="Manifest File"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="project"
          sortable
          header-align="center"
          label="Project"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="path"
          sortable
          header-align="center"
          label="Path"
          width="'25%'">
        </el-table-column>
        <el-table-column
          prop="revision"
          sortable
          :filters="revisionFilters"
          :filter-method="filterRevision"
          header-align="center"
          label="Revision"
          width="'25%'">
        </el-table-column>
      </el-table>
    </el-container>
    <el-footer height="30px">
      <div id="footer">
        <span>Data update time: {{dataUpdateTime}}</span>
        <span> | </span>
        <span>Number of manifest files: {{manifestFilesNum}}</span>
        <span> | </span>
        <span>Number of projects: {{projectsNum}}</span>
        <span> | </span>
        <span>Number of revisions: {{revisionsNum}}</span>
        <span> | </span>
        <span>Press "?" to view help.</span>
      </div>
    </el-footer>
    <help-dialog
      :show="helpDialogVisible"
      @closeDialog="helpDialogVisible=false">
    </help-dialog>
  </div>
</template>

<script>
  import {PROJECT_PATH_SELECT, MANIFEST_REVISION_SELECT, SEPARATOR} from './constants';
  import Help from './Help';

  const SELECT_PROJECT_FLAG = 'project';
  const SELECT_PATH_FLAG = 'path';
  const SELECT_MANIFEST_FLAG = 'manifest';
  const SELECT_REVISION_FLAG = 'revision';

  export default {
    name: 'Main',

    data() {
      return {
        tableHeight: window.innerHeight - 130,
        dataUpdateTime: '1970-01-01 00:00:00',
        manifestFilesNum: '0',
        projectsNum: '0',
        revisionsNum: '0',
        loading: false,
        projectSelect: SELECT_PROJECT_FLAG,
        manifestSelect: SELECT_MANIFEST_FLAG,
        project: '',
        manifest: '',
        projects: [],
        paths: [],
        manifests: [],
        revisions: [],
        tableData: [],
        helpDialogVisible: false,
        revisionFilters: [],
      }
    },
    computed: {
      projectInputPlaceholder() {
        if (this.projectSelect === SELECT_PROJECT_FLAG) {
          return 'Please enter project name'
        } else {
          return 'Please enter project path'
        }
      },
      manifestInputPlaceholder() {
        if (this.manifestSelect === 'manifest') {
          return 'Please enter manifest file name'
        } else {
          return 'Please enter revision'
        }
      },
    },
    watch: {
      projectSelect: function (newValue, oldValue) {
        // 将用户的选择持久化存储到 Local Storage
        localStorage.setItem(PROJECT_PATH_SELECT, newValue);
      },
      manifestSelect: function (newValue, oldValue) {
        // 将用户的选择持久化存储到 Local Storage
        localStorage.setItem(MANIFEST_REVISION_SELECT, newValue);
      },
    },
    mounted() {
      // 从 Local Storage 中读取用户上次的选择
      let projectSelect = localStorage.getItem(PROJECT_PATH_SELECT);
      if (projectSelect === SELECT_PROJECT_FLAG || projectSelect === SELECT_PATH_FLAG) {
        this.projectSelect = projectSelect
      }
      let manifestSelect = localStorage.getItem(MANIFEST_REVISION_SELECT);
      if (manifestSelect === SELECT_MANIFEST_FLAG || manifestSelect === SELECT_REVISION_FLAG) {
        this.manifestSelect = manifestSelect
      }
      // project 自动完成列表
      this.$axios.get('static/projects.list').then((res) => {
        let projects = res.data.split('\n');
        this.projects = projects.map(project => {
          let obj = {};
          obj.value = project;
          return obj
        });
      });
      // path 自动完成列表
      this.$axios.get('static/paths.list').then((res) => {
        let paths = res.data.split('\n');
        this.paths = paths.map(path => {
          let obj = {};
          obj.value = path;
          return obj
        });
      });
      // manifest 自动完成列表
      this.$axios.get('static/manifests.list').then((res) => {
        let manifests = res.data.split('\n');
        this.manifests = manifests.map(manifest => {
          let obj = {};
          obj["value"] = manifest;
          return obj
        });
      });
      // revision 自动完成列表
      this.$axios.get('static/revisions.list').then((res) => {
        let revisions = res.data.split('\n');
        this.revisions = revisions.map(revision => {
          let obj = {};
          obj["value"] = revision;
          return obj
        });
      });
      // 数据更新时间等信息
      this.$axios.get('static/data_info.json').then((res) => {
        this.dataUpdateTime = res.data['update_time'];
        this.manifestFilesNum = res.data['manifest_files_num'];
        this.projectsNum = res.data['projects_num'];
        this.revisionsNum = res.data['revisions_num'];
      });
      // 全局添加按键监听
      document.onkeydown = (event) => {
        return this.keyCheck(event)
      };
      // 解析 URL 参数
      let query = this.$route.query;
      // console.log('query', query);
      let project = query.project;
      let path = query.path;
      let manifest = query.manifest;
      let revision = query.revision;
      console.log('project:', project, 'path:', path, 'manifest:', manifest, 'revision:', revision);
      if (project) {
        this.projectSelect = SELECT_PROJECT_FLAG;
        if (Array.isArray(project)) {
          this.project = project[0]
        } else {
          this.project = project
        }
      }
      if (path) {
        this.projectSelect = SELECT_PATH_FLAG;
        if (Array.isArray(path)) {
          this.project = path[0]
        } else {
          this.project = path
        }
      }
      if (manifest) {
        this.manifestSelect = SELECT_MANIFEST_FLAG;
        if (Array.isArray(manifest)) {
          this.manifest = manifest[0]
        } else {
          this.manifest = manifest
        }
      }
      if (revision) {
        this.manifestSelect = SELECT_REVISION_FLAG;
        if (Array.isArray(revision)) {
          this.manifest = revision[0]
        } else {
          this.manifest = revision
        }
      }
      // 如果 project or path or manifest 不为空，开始搜索
      if (this.project || (this.manifest && this.manifestSelect === SELECT_MANIFEST_FLAG)) {
        this.search()
      }
    },
    methods: {
      keyCheck(event) {
        // 键盘按键监听处理
        // console.log(event);
        let inputProject = this.$refs.input_project;
        let inputManifest = this.$refs.input_manifest;
        if (this.helpDialogVisible) {
          let key = event.key.toLowerCase();
          if (key !== 'shift' && key !== 'control' && key !== 'alt' && key !== 'contextmenu' &&
            key !== "capslock" && key !== "numlock" && key !== "pause") {
            // 隐藏网站帮助
            this.helpDialogVisible = false;
            return false
          }
        } else {
          if (event.key.toLowerCase() === 'enter') {
            this.search();
            // 让输入框失去焦点
            inputProject.$el.querySelectorAll('input')[1].blur();
            inputManifest.$el.querySelector('input').blur();
            return false
          } else if (event.key.toLowerCase() === 'p') {
            // Project 输入框获取焦点
            if (document.activeElement !== inputProject.$el.querySelectorAll('input')[1] &&
              document.activeElement !== inputManifest.$el.querySelector('input')) {
              inputProject.focus();
              // 阻止 按键事件继续传递
              return false
            }
          } else if (event.key.toLowerCase() === 'm') {
            // Manifest 输入框获取焦点
            if (document.activeElement !== inputProject.$el.querySelectorAll('input')[1] &&
              document.activeElement !== inputManifest.$el.querySelector('input')) {
              inputManifest.focus();
              // 阻止 按键事件继续传递
              return false
            }
          } else if (event.key === '?') {
            if (document.activeElement !== inputProject.$el.querySelectorAll('input')[1] &&
              document.activeElement !== inputManifest.$el.querySelector('input')) {
              // 显示网站帮助
              this.helpDialogVisible = !this.helpDialogVisible;
              return false
            }
          }
        }
        return true
      },
      /**
       * 双击单元格触发事件
       * @param row
       * @param column
       * @param cell
       * @param event
       */
      cellDoubleClick(row, column, cell, event) {
        // console.log(row);
        // console.log(column);
        // console.log(cell);
        // console.log(event);
        if (column.property === 'manifest') {
          // 双击的 manifest
          this.manifest = cell.textContent;
          this.manifestSelect = SELECT_MANIFEST_FLAG;
          this.project = '';
          this.loadDataFromManifest(false)
        } else if (column.property === 'project') {
          // 双击的 project
          this.project = cell.textContent;
          this.projectSelect = SELECT_PROJECT_FLAG;
          this.manifest = '';
          this.loadDataFromProject(false)
        } else if (column.property === 'path') {
          // 双击的 path
          this.project = cell.textContent;
          this.projectSelect = SELECT_PATH_FLAG;
          this.manifest = '';
          this.loadDataFromProject(false)
        }
      },
      /**
       * project/path 输入建议（自动完成）
       * @param queryString 输入的查询字符串
       * @param cb 回调函数
       */
      queryProject(queryString, cb) {
        let projects = [];
        if (this.projectSelect === SELECT_PROJECT_FLAG) {
          projects = this.projects;
        } else if (this.projectSelect === SELECT_PATH_FLAG) {
          projects = this.paths;
        }
        let results = queryString ? projects.filter(this.createFilter(queryString)) : projects;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      /**
       * manifest/revision 输入建议（自动完成）
       * @param queryString 输入的查询字符串
       * @param cb 回调函数
       */
      queryManifest(queryString, cb) {
        let manifests = [];
        if (this.manifestSelect === SELECT_MANIFEST_FLAG) {
          manifests = this.manifests;
        } else if (this.manifestSelect === SELECT_REVISION_FLAG) {
          manifests = this.revisions;
        }
        let results = queryString ? manifests.filter(this.createFilter(queryString)) : manifests;
        // 调用 callback 返回建议列表的数据
        cb(results);
      },
      /**
       * 自动完成列表过滤条件
       * @param queryString 输入的查询字符串
       */
      createFilter(queryString) {
        return (restaurant) => {
          return (restaurant.value.toLowerCase().indexOf(queryString.toLowerCase()) >= 0);
        };
      },
      handleSelect(item) {
        // 点击选中建议项时触发
        // console.log(item);
      },
      /**
       * 根据 manifest file 加载数据
       * @param filterProject 是否过滤 project/path
       */
      loadDataFromManifest(filterProject) {
        let manifest = this.manifest.replace(/\//g, SEPARATOR).trim();
        console.log('loadDataFromManifest', manifest);
        // 查询字符串（URL query）
        let queryParams = {query: {'manifest': this.manifest}};
        if (filterProject && this.project) {
          if (this.projectSelect === SELECT_PROJECT_FLAG) {
            queryParams.query.project = this.project;
          } else if (this.projectSelect === SELECT_PATH_FLAG) {
            queryParams.query.path = this.project;
          }
        }
        // 修改 URL query string
        this.$router.replace(queryParams).catch(err => {
          console.log('err', err)
        });
        this.$axios.get('static/manifests/' + manifest).then((res) => {
          // console.log(res.data)
          if (!filterProject || !this.project) {
            this.tableData = res.data;
            if (this.tableData.length === 0) {
              this.$message.error('manifest: ' + this.manifest + ' 不包含 project');
            }
          } else {
            if (this.projectSelect === SELECT_PROJECT_FLAG) {
              this.tableData = res.data.filter((val) => {
                return val.project === this.project
              })
            } else {
              this.tableData = res.data.filter((val) => {
                return val.path === this.project
              })
            }
            if (this.tableData.length === 0) {
              this.$message.error('没有匹配项： manifest: ' + this.manifest + ' AND ' + this.projectSelect + ': ' + this.project);
            }
          }
          this.resetRevisionFilters()
        }).catch(error => {
          console.log(error);
          this.tableData = [];
          this.$message.error('未找到 Manifest 文件：' + this.manifest);
        });
      },
      /**
       * 根据 project name or path 加载数据
       * @param filterRevision 是否过滤 revision
       */
      loadDataFromProject(filterRevision) {
        let project = this.project.replace(/\//g, SEPARATOR, -1).trim();
        console.log('loadDataFromProject', project);
        let url = '';
        // 查询字符串（URL query）
        let queryParams = {query: {}};
        if (this.projectSelect === SELECT_PROJECT_FLAG) {
          queryParams.query.project = this.project;
          url = 'static/projects/' + project
        } else {
          queryParams.query.path = this.project;
          url = 'static/paths/' + project
        }
        if (filterRevision && this.manifest) {
          queryParams.query.revision = this.manifest;
        }
        // 修改 URL query string
        this.$router.replace(queryParams).catch(err => {
          console.log('err', err)
        });
        this.$axios.get(url).then((res) => {
          // console.log(res.data)
          if (!filterRevision || !this.manifest) {
            this.tableData = res.data;
          } else {
            this.tableData = res.data.filter((val) => {
              return val.revision === this.manifest
            });
            if (this.tableData.length === 0) {
              this.$message.error('没有匹配项： ' + this.projectSelect + ': ' + this.project + ' AND revision: ' + this.manifest);
            }
          }
          this.resetRevisionFilters()
        }).catch(error => {
          console.log(error);
          this.tableData = [];
          if (this.projectSelect === SELECT_PROJECT_FLAG) {
            this.$message.error('未找到 Project：' + this.project);
          } else {
            this.$message.error('未找到 Path：' + this.project);
          }
        });
      },
      /**
       * 执行搜索
       */
      search() {
        this.loading = true;
        this.project = this.project.trim();
        this.manifest = this.manifest.trim();
        if (!this.project && (!this.manifest || this.manifestSelect === SELECT_REVISION_FLAG)) {
          this.$message.error('Project/Path 和 Manifest 需要至少填写一项');
        } else if (!this.project && this.manifestSelect === SELECT_MANIFEST_FLAG) {
          // manifest 有值
          this.loadDataFromManifest(false)
        } else if (!this.manifest) {
          // project 有值
          this.loadDataFromProject(false)
        } else {
          // project 和 manifest 都有值
          if (this.manifestSelect === SELECT_MANIFEST_FLAG) {
            this.loadDataFromManifest(true)
          } else if (this.manifestSelect === SELECT_REVISION_FLAG) {
            this.loadDataFromProject(true)
          }
        }
        this.loading = false;
      },
      /**
       * 重置 revision 过滤列表
       */
      resetRevisionFilters() {
        // 清除过滤
        this.$refs.main_table.clearFilter();
        this.revisionFilters = [];
        let revisionSet = new Set();
        this.tableData.forEach((value) => {
          revisionSet.add(value.revision)
        });
        revisionSet.forEach((value) => {
          let obj = {};
          obj.text = value;
          obj.value = value;
          this.revisionFilters.push(obj)
        });
      },
      /**
       * revision 过滤方法
       * @param value
       * @param row
       * @param column
       * @returns {boolean}
       */
      filterRevision(value, row, column) {
        const property = column['property'];
        return row[property] === value;
      }
    },
    components: {
      'help-dialog': Help
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
  #main-container {
    margin: 0 20px 0 20px;
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

  #main-container .el-select .el-input {
    width: 130px;
  }

  #main-container .el-table td {
    padding: 8px 0;
  }

  #main-container .el-table th {
    padding: 4px 0;
  }

  #main-container .el-footer {
    display: flex;
    flex-direction: column;
    -webkit-align-items: center;
    align-items: center;
    -webkit-justify-content: center;
    justify-content: center;
  }

  #main-container #footer {
    font-size: 12px;
    margin: 0;
    padding: 0;
    color: #afb4bf;
  }
</style>
