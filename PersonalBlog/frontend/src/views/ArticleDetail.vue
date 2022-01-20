<template>
  <BlogHeader/>
      <div v-if="article !== null" class="grid-container" style="padding-top: 100px">
        <div>
            <h1 id="title">{{ article.title }}</h1>
            <p id="subtitle">
                本文由 {{ article.author.username }} 发布于 {{ formatted_time(article.created) }}
            </p>
            <div v-html="article.body_html" class="article-body"></div>
        </div>
        <div>
            <h3>目录</h3>
            <div v-html="article.toc_html" class="toc"></div>
        </div>
    </div>
  <BlogFooter/>
</template>

<script>
import BlogFooter from "@/components/BlogFooter";
import BlogHeader from "@/components/BlogHeader";
import axios from "axios";
export default {
  name: "ArticleDetail",
  components:{BlogHeader,BlogFooter},
  data: function (){
    return {
      article:null
    }
  },
  mounted() {
    axios
        .get(''+this.$route.params.id)
        .then(response => (this.article = response.data))
  },
  methods: {
    formatted_time:function (iso_date_string){
      const date = new Date(iso_date_string);
      return date.toLocaleString()
    }
  }
}
</script>
<style scoped>
    .grid-container {
        display: grid;
        grid-template-columns: 3fr 1fr;
    }


    #title {
        text-align: center;
        font-size: x-large;
    }

    #subtitle {
        text-align: center;
        color: gray;
        font-size: small;
    }

</style>
<style>
    .article-body p img {
        max-width: 100%;
        border-radius: 50px;
        box-shadow: gray 0 0 20px;
    }

    .toc ul {
        list-style-type: none;
    }

    .toc a {
        color: gray;
    }
    .toc{
      background-color: lightgrey;
    }
    pre { line-height: 125%; }
    td.linenos .normal { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
    span.linenos { color: inherit; background-color: transparent; padding-left: 5px; padding-right: 5px; }
    td.linenos .special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
    span.linenos.special { color: #000000; background-color: #ffffc0; padding-left: 5px; padding-right: 5px; }
    .codehilite .hll { background-color: #49483e }
    .codehilite { background: #272822; color: #f8f8f2;font-size: 15px }
    .codehilite .c { color: #75715e } /* Comment */
    .codehilite .err { color: #960050; background-color: #1e0010 } /* Error */
    .codehilite .esc { color: #f8f8f2 } /* Escape */
    .codehilite .g { color: #f8f8f2 } /* Generic */
    .codehilite .k { color: #66d9ef } /* Keyword */
    .codehilite .l { color: #ae81ff } /* Literal */
    .codehilite .n { color: #f8f8f2 } /* Name */
    .codehilite .o { color: #f92672 } /* Operator */
    .codehilite .x { color: #f8f8f2 } /* Other */
    .codehilite .p { color: #f8f8f2 } /* Punctuation */
    .codehilite .ch { color: #75715e } /* Comment.Hashbang */
    .codehilite .cm { color: #75715e } /* Comment.Multiline */
    .codehilite .cp { color: #75715e } /* Comment.Preproc */
    .codehilite .cpf { color: #75715e } /* Comment.PreprocFile */
    .codehilite .c1 { color: #75715e } /* Comment.Single */
    .codehilite .cs { color: #75715e } /* Comment.Special */
    .codehilite .gd { color: #f92672 } /* Generic.Deleted */
    .codehilite .ge { color: #f8f8f2; font-style: italic } /* Generic.Emph */
    .codehilite .gr { color: #f8f8f2 } /* Generic.Error */
    .codehilite .gh { color: #f8f8f2 } /* Generic.Heading */
    .codehilite .gi { color: #a6e22e } /* Generic.Inserted */
    .codehilite .go { color: #66d9ef } /* Generic.Output */
    .codehilite .gp { color: #f92672; font-weight: bold } /* Generic.Prompt */
    .codehilite .gs { color: #f8f8f2; font-weight: bold } /* Generic.Strong */
    .codehilite .gu { color: #75715e } /* Generic.Subheading */
    .codehilite .gt { color: #f8f8f2 } /* Generic.Traceback */
    .codehilite .kc { color: #66d9ef } /* Keyword.Constant */
    .codehilite .kd { color: #66d9ef } /* Keyword.Declaration */
    .codehilite .kn { color: #f92672 } /* Keyword.Namespace */
    .codehilite .kp { color: #66d9ef } /* Keyword.Pseudo */
    .codehilite .kr { color: #66d9ef } /* Keyword.Reserved */
    .codehilite .kt { color: #66d9ef } /* Keyword.Type */
    .codehilite .ld { color: #e6db74 } /* Literal.Date */
    .codehilite .m { color: #ae81ff } /* Literal.Number */
    .codehilite .s { color: #e6db74 } /* Literal.String */
    .codehilite .na { color: #a6e22e } /* Name.Attribute */
    .codehilite .nb { color: #f8f8f2 } /* Name.Builtin */
    .codehilite .nc { color: #a6e22e } /* Name.Class */
    .codehilite .no { color: #66d9ef } /* Name.Constant */
    .codehilite .nd { color: #a6e22e } /* Name.Decorator */
    .codehilite .ni { color: #f8f8f2 } /* Name.Entity */
    .codehilite .ne { color: #a6e22e } /* Name.Exception */
    .codehilite .nf { color: #a6e22e } /* Name.Function */
    .codehilite .nl { color: #f8f8f2 } /* Name.Label */
    .codehilite .nn { color: #f8f8f2 } /* Name.Namespace */
    .codehilite .nx { color: #a6e22e } /* Name.Other */
    .codehilite .py { color: #f8f8f2 } /* Name.Property */
    .codehilite .nt { color: #f92672 } /* Name.Tag */
    .codehilite .nv { color: #f8f8f2 } /* Name.Variable */
    .codehilite .ow { color: #f92672 } /* Operator.Word */
    .codehilite .w { color: #f8f8f2 } /* Text.Whitespace */
    .codehilite .mb { color: #ae81ff } /* Literal.Number.Bin */
    .codehilite .mf { color: #ae81ff } /* Literal.Number.Float */
    .codehilite .mh { color: #ae81ff } /* Literal.Number.Hex */
    .codehilite .mi { color: #ae81ff } /* Literal.Number.Integer */
    .codehilite .mo { color: #ae81ff } /* Literal.Number.Oct */
    .codehilite .sa { color: #e6db74 } /* Literal.String.Affix */
    .codehilite .sb { color: #e6db74 } /* Literal.String.Backtick */
    .codehilite .sc { color: #e6db74 } /* Literal.String.Char */
    .codehilite .dl { color: #e6db74 } /* Literal.String.Delimiter */
    .codehilite .sd { color: #e6db74 } /* Literal.String.Doc */
    .codehilite .s2 { color: #e6db74 } /* Literal.String.Double */
    .codehilite .se { color: #ae81ff } /* Literal.String.Escape */
    .codehilite .sh { color: #e6db74 } /* Literal.String.Heredoc */
    .codehilite .si { color: #e6db74 } /* Literal.String.Interpol */
    .codehilite .sx { color: #e6db74 } /* Literal.String.Other */
    .codehilite .sr { color: #e6db74 } /* Literal.String.Regex */
    .codehilite .s1 { color: #e6db74 } /* Literal.String.Single */
    .codehilite .ss { color: #e6db74 } /* Literal.String.Symbol */
    .codehilite .bp { color: #f8f8f2 } /* Name.Builtin.Pseudo */
    .codehilite .fm { color: #a6e22e } /* Name.Function.Magic */
    .codehilite .vc { color: #f8f8f2 } /* Name.Variable.Class */
    .codehilite .vg { color: #f8f8f2 } /* Name.Variable.Global */
    .codehilite .vi { color: #f8f8f2 } /* Name.Variable.Instance */
    .codehilite .vm { color: #f8f8f2 } /* Name.Variable.Magic */
    .codehilite .il { color: #ae81ff } /* Literal.Number.Integer.Long */

</style>