<template>
  <span class="feather-icon-wrapper" :class="sizeClass" v-html="iconHtml"></span>
</template>

<script setup>
import { computed, onMounted } from 'vue';
import feather from 'feather-icons';

// Ensure Feather icons are initialized
onMounted(() => {
  feather.replace();
});

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  size: {
    type: String,
    default: 'md'
  },
  strokeWidth: {
    type: Number,
    default: 2
  },
  color: {
    type: String,
    default: 'currentColor'
  }
});

const sizeClass = computed(() => `icon-${props.size}`);

const iconHtml = computed(() => {
  if (!feather.icons[props.name]) {
    console.warn(`Icon "${props.name}" not found in Feather Icons`);
    return '';
  }
  
  return feather.icons[props.name].toSvg({
    'stroke-width': props.strokeWidth,
    color: props.color,
    width: '100%',
    height: '100%'
  });
});
</script>

<style scoped>
.feather-icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.icon-xs {
  width: 16px;
  height: 16px;
}

.icon-sm {
  width: 20px;
  height: 20px;
}

.icon-md {
  width: 24px;
  height: 24px;
}

.icon-lg {
  width: 32px;
  height: 32px;
}

.icon-xl {
  width: 40px;
  height: 40px;
}
</style> 