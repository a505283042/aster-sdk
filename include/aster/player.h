/* SPDX-License-Identifier: MIT */
#ifndef ASTER_PLAYER_H
#define ASTER_PLAYER_H
#include "system.h"
/* ABI 4.4: optional, system-owned media session; survives APP exit. */
#define ASTER_PLAYER_CAP_WAV 1u
#define ASTER_PLAYER_CAP_FLAC 2u
#define ASTER_PLAYER_CAP_BT_SINK 4u
#define ASTER_PLAYER_CAP_REMOTE 8u
#define ASTER_PLAYER_CAP_BT_SOURCE 16u
#define ASTER_PLAYER_CAP_SPECTRUM 32u
#define ASTER_PLAYER_LOCAL 1u
#define ASTER_PLAYER_BLUETOOTH 2u
#define ASTER_PLAYER_IDLE 0u
#define ASTER_PLAYER_OPENING 1u
#define ASTER_PLAYER_PLAYING 2u
#define ASTER_PLAYER_PAUSED 3u
#define ASTER_PLAYER_ENDED 4u
#define ASTER_PLAYER_ERROR 5u
#define ASTER_PLAYER_STOPPING 6u
#define ASTER_PLAYER_F_CONNECTED 1u
#define ASTER_PLAYER_F_REMOTE 2u
#define ASTER_PLAYER_F_BT_OUTPUT 4u
#define ASTER_PLAYER_PLAY_FILE 1u
#define ASTER_PLAYER_PAUSE 2u
#define ASTER_PLAYER_RESUME 3u
#define ASTER_PLAYER_STOP 4u
#define ASTER_PLAYER_SEEK 5u
#define ASTER_PLAYER_BT_ON 6u
#define ASTER_PLAYER_BT_OFF 7u
#define ASTER_PLAYER_NEXT 8u
#define ASTER_PLAYER_PREVIOUS 9u
#define ASTER_PLAYER_SOURCE_ON 10u
#define ASTER_PLAYER_BT_SCAN 11u
#define ASTER_PLAYER_BT_CONNECT 12u
#define ASTER_PLAYER_BT_DISCONNECT 13u
#define ASTER_PLAYER_OUTPUT_WIRED 1u
#define ASTER_PLAYER_OUTPUT_BLUETOOTH 2u

typedef struct {
    uint32_t size, version, capabilities, mode, state, flags;
    int32_t error;
    uint32_t rate, bits, channels, position_ms, duration_ms;
    char title[192], artist[128], album[128], path[256], device[32];
    /* CAP_SPECTRUM: reserved[0] is left and reserved[1] is right. Each holds
  * four unsigned 8-bit levels, lowest band in the least significant byte. */
    uint32_t reserved[4];
} aster_player_info_t;

typedef struct {
    uint32_t size, version, command, value;
    char path[256]; /* PLAY_FILE: absolute APP sandbox path, NUL terminated. */
} aster_player_request_t;

ASTER_I("aster_player_get_info")
int32_t aster_player_get_info(aster_player_info_t *info, uint32_t size);
ASTER_I("aster_player_control")
int32_t aster_player_control(const aster_player_request_t *request, uint32_t size);
/* ABI 4.5: bounded Classic audio-device discovery snapshot. Connect uses the
 * displayed address in request.path, never a possibly stale list index. */
#define ASTER_PLAYER_BT_DEVICES_MAX 8u
#define ASTER_PLAYER_BT_IDLE 0u
#define ASTER_PLAYER_BT_SCANNING 1u
#define ASTER_PLAYER_BT_CONNECTING 2u
#define ASTER_PLAYER_BT_CONNECTED 3u
#define ASTER_PLAYER_BT_ERROR 4u
#define ASTER_PLAYER_BT_STOPPING 5u

typedef struct {
    char address[18], name[62];
    int32_t rssi;
    uint32_t flags;
} aster_player_bt_device_t;

typedef struct {
    uint32_t size, version, generation, state, count;
    int32_t error;
    uint32_t output_rate, queued_bytes;
    aster_player_bt_device_t devices[ASTER_PLAYER_BT_DEVICES_MAX];
} aster_player_bt_list_t;

ASTER_I("aster_player_bt_list")
int32_t aster_player_bt_list(aster_player_bt_list_t *list, uint32_t size);
#endif
