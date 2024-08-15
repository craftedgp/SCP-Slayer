#version 330

in vec2 frag_uv;
out vec4 frag_color;

uniform sampler2D tex;
uniform float blur_amount;

void main() {
    vec2 tex_offset = vec2(1.0) / textureSize(tex, 0); // gets size of single texel
    vec4 color = vec4(0.0);
    
    // Applying a simple 9-tap box blur
    for(int x = -1; x <= 1; x++) {
        for(int y = -1; y <= 1; y++) {
            vec2 offset = vec2(float(x), float(y)) * tex_offset * blur_amount;
            color += texture(tex, frag_uv + offset);
        }
    }
    
    color /= 9.0;
    frag_color = color;
}
