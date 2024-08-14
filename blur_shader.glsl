#version 330 core

out vec4 FragColor;
in vec2 TexCoords;

uniform sampler2D screenTexture;
uniform vec2 resolution;
uniform float blurAmount;

void main()
{
    vec2 texOffset = blurAmount / resolution; // Size of one pixel times blur amount
    vec3 result = vec3(0.0);

    // 5-tap blur: center and four adjacent pixels
    result += texture(screenTexture, TexCoords).rgb * 0.4;  // Main pixel
    result += texture(screenTexture, TexCoords + vec2(texOffset.x, 0.0)).rgb * 0.15;
    result += texture(screenTexture, TexCoords - vec2(texOffset.x, 0.0)).rgb * 0.15;
    result += texture(screenTexture, TexCoords + vec2(0.0, texOffset.y)).rgb * 0.15;
    result += texture(screenTexture, TexCoords - vec2(0.0, texOffset.y)).rgb * 0.15;

    FragColor = vec4(result, 1.0);
}
