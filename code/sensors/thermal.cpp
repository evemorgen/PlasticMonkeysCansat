#include <stdint.h>
#include <iostream>
#include <cstring>
#include <string>
#include <fstream>
#include <chrono>
#include <ctime>
#include <thread>
#include "headers/MLX90640_API.h"

#define FMT_STRING " %.0f"
#define MLX_I2C_ADDR 0x33

int main(){
    int state = 0;
    static uint16_t eeMLX90640[832];
    float emissivity = 1;
    uint16_t frame[834];
    static float image[768];
    float eTa;
    static uint16_t data[768*sizeof(float)];

    std::fstream fs;
    std::ofstream output;

    MLX90640_SetDeviceMode(MLX_I2C_ADDR, 0);
    MLX90640_SetSubPageRepeat(MLX_I2C_ADDR, 0);
    MLX90640_SetRefreshRate(MLX_I2C_ADDR, 0b010);
    MLX90640_SetChessMode(MLX_I2C_ADDR);
    //MLX90640_SetSubPage(MLX_I2C_ADDR, 0);
    
    paramsMLX90640 mlx90640;
    MLX90640_DumpEE(MLX_I2C_ADDR, eeMLX90640);
    MLX90640_ExtractParameters(eeMLX90640, &mlx90640);

    int refresh = MLX90640_GetRefreshRate(MLX_I2C_ADDR);
    
    int frames = 30;
    int subpage;
    static float mlx90640To[768];
    do {
        state = !state;
        //printf("State: %d \n", state);
        MLX90640_GetFrameData(MLX_I2C_ADDR, frame);
        MLX90640_InterpolateOutliers(frame, eeMLX90640);
        eTa = MLX90640_GetTa(frame, &mlx90640);
        subpage = MLX90640_GetSubPageNumber(frame);
        MLX90640_CalculateTo(frame, &mlx90640, emissivity, eTa, mlx90640To);
        //printf("Subpage: %d\n", subpage);
        //MLX90640_SetSubPage(MLX_I2C_ADDR,!subpage);

        std::time_t result = std::time(nullptr) % 86400;
        std::string stamp = std::to_string(result);
        output.open("/home/pi/thermal/" + stamp + ".txt");
        for(int x = 0; x < 32; x++){
            for(int y = 0; y < 24; y++){
                //std::cout << image[32 * y + x] << ",";
                float val = mlx90640To[32 * (23-y) + x];
                val *= 10;
                //printf(FMT_STRING, val);
                output << std::to_string((int)val) << " ";
            }
            output << std::endl;
        }
        output.close();
        std::this_thread::sleep_for(std::chrono::milliseconds(5000));
        std::cout << std::endl;
        //printf("\x1b[33A");
    } while (1);
    return 0;
}
