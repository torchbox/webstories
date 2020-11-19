import re
from bleach.sanitizer import Cleaner


ALLOWED_STORY_PAGE_TAGS = [
    'amp-story-page', 'amp-story-grid-layer', 'amp-story-cta-layer',

    # allowed child elements of amp-story-grid-layer as per
    # https://github.com/ampproject/amphtml/blob/b950dfa82d8f72ece43535249bc1a7b645dfb0a1/extensions/amp-story/validator-amp-story.protoascii#L647
    'a', 'abbr', 'address', 'article', 'aside', 'b', 'bdi', 'bdo', 'blockquote', 'br', 'caption',
    'cite', 'code', 'col', 'colgroup', 'data', 'dd', 'del', 'dfn', 'div', 'dl', 'dt', 'em',
    'figcaption', 'figure', 'footer', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'header', 'hgroup', 'hr', 'i', 'ins', 'kbd', 'li', 'main', 'mark', 'nav', 'noscript',
    'ol', 'p', 'pre', 'q', 'rp', 'rt', 'rtc', 'ruby', 's', 'samp', 'script', 'section', 'small',
    'source', 'span', 'strong', 'sub', 'sup', 'table', 'tbody', 'td', 'template', 'tfoot', 'th',
    'thead', 'time', 'tr', 'track', 'u', 'ul', 'var', 'wbr',

    'amp-analytics', 'amp-audio', 'amp-date-countdown', 'amp-experiment', 'amp-fit-text',
    'amp-font', 'amp-gist', 'amp-google-vrview-image', 'amp-img', 'amp-install-serviceworker',
    'amp-list', 'amp-live-list', 'amp-pixel', 'amp-state', 'amp-story-360',
    'amp-story-interactive-binary-poll', 'amp-story-interactive-poll',
    'amp-story-interactive-quiz', 'amp-story-interactive-results', 'amp-timeago', 'amp-twitter',
    'amp-video',

    # additionally allowed in amp-story-cta-layer as per
    # https://github.com/ampproject/amphtml/blob/b950dfa82d8f72ece43535249bc1a7b645dfb0a1/extensions/amp-story/validator-amp-story.protoascii#L535
    'amp-call-tracking', 'button',
]

# SVG not supported yet (because defining their allowed attributes is non-trivial)
SVG_TAGS = [
    'circle', 'clippath', 'defs', 'desc', 'ellipse', 'fecolormatrix', 'fecomposite', 'feflood',
    'fegaussianblur', 'femerge', 'femergenode', 'feoffset', 'filter', 'g', 'glyph', 'glyphref',
    'hkern', 'image', 'line', 'lineargradient', 'marker', 'mask', 'metadata', 'path', 'pattern', 'polygon',
    'polyline', 'radialgradient', 'rect', 'solidcolor', 'stop', 'svg', 'switch', 'symbol', 'text',
    'textpath', 'title', 'tref', 'tspan', 'use', 'view', 'vkern',
]

# global attributes as per
# https://github.com/ampproject/amphtml/blob/b950dfa82d8f72ece43535249bc1a7b645dfb0a1/validator/validator-main.protoascii#L5292
GLOBAL_ATTRIBUTES = [
    'itemid', 'itemprop', 'itemref', 'itemscope', 'itemtype',
    'about', 'content', 'datatype', 'inlist', 'prefix', 'property', 'rel', 'resource', 'rev',
    'style', 'typeof', 'vocab', 'accesskey', 'class', 'dir', 'draggable', 'hidden', 'id',
    'lang', 'slot', 'tabindex', 'title', 'translate',
    'aria-activedescendant', 'aria-atomic', 'aria-autocomplete', 'aria-busy', 'aria-checked',
    'aria-controls', 'aria-current', 'aria-describedby', 'aria-disabled', 'aria-dropeffect',
    'aria-expanded', 'aria-flowto', 'aria-grabbed', 'aria-haspopup', 'aria-hidden', 'aria-invalid',
    'aria-label', 'aria-labelledby', 'aria-level', 'aria-live', 'aria-multiline', 'aria-multiselectable',
    'aria-orientation', 'aria-owns', 'aria-posinset', 'aria-pressed', 'aria-readonly', 'aria-relevant',
    'aria-required', 'aria-selected', 'aria-setsize', 'aria-sort', 'aria-valuemax', 'aria-valuemin',
    'aria-valuenow', 'aria-valuetext',
    'on', 'role', 'placeholder', 'fallback', 'overflow',
]

ANIMATION_ATTRIBUTES = [
    'animate-in', 'animate-in-duration', 'animate-in-timing-function', 'animate-in-delay',
    'animate-in-after', 'scale-start', 'scale-end', 'translate-x', 'translate-y',
]

GLOBAL_ATTRIBUTES += ANIMATION_ATTRIBUTES

DATA_ATTR_RE = re.compile(r'^data-[A-Za-z0-9-_:.]*$')


class AttributeRule:
    def __init__(self, attrs=None):
        self.allowed_attributes = set((attrs or []) + GLOBAL_ATTRIBUTES)

    def __call__(self, tag, attr_name, attr_value):
        return (
            attr_name in self.allowed_attributes
            or DATA_ATTR_RE.match(attr_name)
        )


COMMON_ATTRIBUTES = [
    'fallback', 'heights', 'layout', 'media', 'noloading', 'on', 'placeholder', 'sizes',
    'width', 'height',
]

INTERACTIVE_ATTRIBUTES = [
    'endpoint', 'theme', 'chip-style', 'prompt-text', 'prompt-size',
    'option-1-text', 'option-2-text', 'option-3-text', 'option-4-text',
    'option-1-confetti', 'option-2-confetti', 'option-3-confetti', 'option-4-confetti',
    'option-1-results-category', 'option-2-results-category',
    'option-3-results-category', 'option-4-results-category',
    'option-1-results-threshold', 'option-2-results-threshold',
    'option-3-results-threshold', 'option-4-results-threshold',
]

ALLOWED_STORY_PAGE_ATTRIBUTES = {
    'a': AttributeRule(['border', 'download', 'href', 'hreflang', 'media', 'referrerpolicy', 'rel', 'role', 'tabindex', 'target', 'type', 'show-tooltip', 'name']),
    'abbr': AttributeRule([]),
    'address': AttributeRule([]),
    'article': AttributeRule([]),
    'aside': AttributeRule([]),
    'bdi': AttributeRule([]),
    'bdo': AttributeRule(['dir']),
    'blockquote': AttributeRule(['align', 'cite']),
    'br': AttributeRule([]),
    'button': AttributeRule(['disabled', 'role', 'tabindex']),
    'caption': AttributeRule([]),
    'cite': AttributeRule([]),
    'code': AttributeRule([]),
    'col': AttributeRule(['span']),
    'colgroup': AttributeRule(['span']),
    'data': AttributeRule([]),
    'dd': AttributeRule([]),
    'del': AttributeRule(['datetime', 'cite']),
    'dfn': AttributeRule([]),
    'div': AttributeRule(['align']),
    'dl': AttributeRule([]),
    'dt': AttributeRule([]),
    'em': AttributeRule([]),
    'figcaption': AttributeRule([]),
    'figure': AttributeRule([]),
    'footer': AttributeRule([]),
    'h1': AttributeRule(['align']),
    'h2': AttributeRule(['align']),
    'h3': AttributeRule(['align']),
    'h4': AttributeRule(['align']),
    'h5': AttributeRule(['align']),
    'h6': AttributeRule(['align']),
    'header': AttributeRule([]),
    'hgroup': AttributeRule([]),
    'hr': AttributeRule([]),
    'i': AttributeRule([]),
    'ins': AttributeRule(['datetime', 'cite']),
    'kbd': AttributeRule([]),
    'li': AttributeRule(['value']),
    'main': AttributeRule([]),
    'mark': AttributeRule([]),
    'nav': AttributeRule([]),
    'noscript': AttributeRule([]),
    'ol': AttributeRule(['reversed', 'start', 'type']),
    'p': AttributeRule(['align']),
    'pre': AttributeRule([]),
    'q': AttributeRule(['cite']),
    'rp': AttributeRule([]),
    'rt': AttributeRule([]),
    'rtc': AttributeRule([]),
    'ruby': AttributeRule([]),
    's': AttributeRule([]),
    'samp': AttributeRule([]),
    'script': AttributeRule(['async', 'src', 'custom-element', 'type']),
    'section': AttributeRule([]),
    'small': AttributeRule([]),
    'source': AttributeRule(['media', 'src', 'type']),
    'span': AttributeRule([]),
    'strong': AttributeRule([]),
    'sub': AttributeRule([]),
    'sup': AttributeRule([]),
    'table': AttributeRule(['align', 'bgcolor', 'border', 'cellpadding', 'cellspacing', 'sortable']),
    'tbody': AttributeRule([]),
    'td': AttributeRule([
        'align', 'bgcolor', 'colspan', 'headers', 'height', 'rowspan', 'valign', 'width',
    ]),
    'template': AttributeRule([]),
    'tfoot': AttributeRule([]),
    'th': AttributeRule([
        'abbr', 'align', 'bgcolor', 'colspan', 'headers', 'height', 'rowspan', 'scope', 'sorted',
        'valign', 'width',
    ]),
    'thead': AttributeRule([]),
    'time': AttributeRule(['datetime', 'pubdate']),
    'tr': AttributeRule(['align', 'bgcolor', 'height', 'valign']),
    'track': AttributeRule(['default', 'kind', 'label', 'src', 'srclang']),
    'u': AttributeRule([]),
    'ul': AttributeRule([]),
    'var': AttributeRule([]),
    'wbr': AttributeRule([]),

    'amp-story-page': AttributeRule(['auto-advance-after', 'background-audio']),
    'amp-story-cta-layer': AttributeRule([]),
    'amp-story-grid-layer': AttributeRule(['template', 'grid-area', 'aspect-ratio']),

    'amp-analytics': AttributeRule(['type', 'config']),
    'amp-audio': AttributeRule([
        'src', 'preload', 'autoplay', 'loop', 'muted', 'controlsList',
        'artwork', 'artist', 'album', 'title',
    ]),
    'amp-call-tracking': AttributeRule(['config']),
    'amp-date-countdown': AttributeRule([
        'end-date', 'timestamp-ms', 'timestamp-seconds', 'timeleft-ms', 'offset-seconds',
        'when-ended', 'locale', 'biggest-unit',
    ]),
    'amp-experiment': AttributeRule([]),
    'amp-fit-text': AttributeRule(['min-font-size', 'max-font-size'] + COMMON_ATTRIBUTES),
    'amp-font': AttributeRule([
        'font-family', 'timeout', 'on-load-add-class', 'on-error-add-class',
        'on-error-remove-class', 'font-weight', 'font-style', 'font-variant', 'layout',
    ]),
    'amp-gist': AttributeRule(['layout', 'height']),
    'amp-google-vrview-image': AttributeRule(['src', 'width', 'height', 'layout', 'stereo', 'yaw', 'yaw-only']),
    'amp-img': AttributeRule(
        ['src', 'srcset', 'sizes', 'alt', 'attribution', 'height', 'width'] + COMMON_ATTRIBUTES
    ),
    'amp-install-serviceworker': AttributeRule(['src', 'layout']),
    'amp-list': AttributeRule([
        'src', 'credentials', 'items', 'max-items', 'single-item', 'xssi-prefix',
        'reset-on-refresh', 'load-more', 'load-more-bookmark'
    ] + COMMON_ATTRIBUTES),
    'amp-live-list': AttributeRule(['disabled']),
    'amp-pixel': AttributeRule(['src', 'referrerpolicy', 'allow-ssr-img'] + COMMON_ATTRIBUTES),
    'amp-state': AttributeRule(['src']),
    'amp-story-interactive-binary-poll': AttributeRule(INTERACTIVE_ATTRIBUTES),
    'amp-story-interactive-poll': AttributeRule(INTERACTIVE_ATTRIBUTES),
    'amp-story-interactive-quiz': AttributeRule(INTERACTIVE_ATTRIBUTES),
    'amp-story-interactive-results': AttributeRule(INTERACTIVE_ATTRIBUTES),
    'amp-twitter': AttributeRule(COMMON_ATTRIBUTES),
    'amp-video': AttributeRule([
        'src', 'poster', 'autoplay', 'controls', 'controlsList', 'loop', 'crossorigin',
        'disableremoteplayback', 'muted', 'noaudio', 'rotate-to-fullscreen',
        'artwork', 'artist', 'album', 'title',
    ] + COMMON_ATTRIBUTES),
}


class StoryPageCleaner(Cleaner):
    def __init__(self, **kwargs):
        opts = {
            'tags': ALLOWED_STORY_PAGE_TAGS,
            'attributes': ALLOWED_STORY_PAGE_ATTRIBUTES,
            'strip': True,
        }
        opts.update(kwargs)
        super().__init__(**opts)
