import os
import sys
import io
import json
import base64
import zipfile
import subprocess
from typing import Tuple, Optional, Dict, Any

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk


VANILLA_SHIELD_NOPATTERN_HEX = "89504e470d0a1a0a0000000d4948445200000040000000400806000000aa6971de0000045e494441547801ec584d481551143ebe9a4bbecad7cbe897e8c70afa8356b56813116dda1404410b77461bab5dcbc0453fd0a2b255b67211082e224a225c56ab42110c22529354a24c9f3fcf30c1de77f58c67eebc51877c32ce5cf19b73ee77cebdef9e73cf9c99f75254f87b58df301d06d76edc9c0e83c24704fe5fba543d2d11e85822430a8163ed8dd90c2d06f0adaada4713f9bc06c640ba3c4de001e8e000f8d55ca99d865e0c15990c4914f32925a72b0081f7be7b4c8c8e96db5a2f26e1cb1b1aef6ea181b667f4abb399bebe7f4a9d6feed3dbe63aeafdd0e8f2c39f9fb37b24a54e00efecdbf71f349c1ba1dce884a6a404dff77354f3b894a7d3b46ecd6aa81a8e525ae2f2777212c2b5c3571311bca406fafbdd6d65f79ea69ebe413d46c05a99bd38db4e1207364bf9c4d0489eb215691f1f65c253015ded2f6972724aef7743a682c6fe4ce98a00d1d3f1dab52169b8cf61874d5602c6128e52045fc9497d24972309695b0edd930047293ab0678b0e1c1f2e033bbc6f07ad5d37ffe922799c14cc97fa9933e774b7474304d0f9c1c10f181c9ca93cd800b64302f029053c09c007e0e421e52d2003818dc10932ed4884e9535959494d4d8dd4f0a45e033a387e0240071764e7f5965aa6f213f945ad2913b298098e529e9e8140cd7992933afb15e3d8b654d253013b0f9da5f64fddbeb571d2ced6b926c849334f1e1365a39495005b14e1260027dc259a20362b03fcf2f185db04616370903270b641f21a6874184b484eeaec538c63db52499d80df4339bd9ea3141d3fb65febfc0e800182d8bda3523741f605cf080a1ef6f1b1995b0c4daed0cca8d0e034a08343900074704176ac550ae8042cb4306e81623e1cb8a314396aee4508be6ce327476bebabb242932b2b34390de8cc493dc88e354b8194f98cc6ad800fcaac2f87d040056825c4c551de848498baacae6e05e0f18726c86f82d8853c79d90461031ce50fd2515e4eae813951839b006c8c9ba0b9698c839a20e671b9438f3accfd7912e0a89937417692a5cf4d103679db28b55a3f1dcc24f058ae81b951436adbf6ed0bee29ea412c18c03c0e9e0a40a9c31701cbc7203806be0871d2f894d9b612a54e0082c2e6b355735f873196309b20bf0db24fd00b119264faf29c28489d00de4857dbdcd761e6b812829a2007cefe3c66c97c54a59b003cff1da568cba60adf5e716b640b3f74481b7eeb5b4c90f081af6fd188106e0256edba409b0e5fa43555e77d121cb0f1c865cfb6371fbd48bb4e546b1c3c75954e5faed380ce3c7c3c932236485dafad29bb7be796c6a307f7cae603fb610ebfb2b23f6ce001e8ccb35fc4e276b7e35680cb244cb10948d881fbc2b515e04b49c2085b01093b705fb8b1af005fc406611360242471435b01893b7223605b0146421237b41590b8233702b61560242471435b01893b7223605b0146421237b41510b7230f1b8fad80b0198b9bbfad80b89d68d8786c0584cd58dcfc6d05c4ed44c3c6632b206cc6e2e66f2b206e271a361e5b01613316377f5b012bfd44ff77ffff000000ffff22b80a510000000649444154030034da559fee4993ba0000000049454e44ae426082"

VANILLA_SHIELD_BASE_HEX = "89504e470d0a1a0a0000000d4948445200000040000000400806000000aa6971de000003d5494441547801ec583d4c1441147eb76127c74920482291c6021b0b0b2b4c6c94d0d99a9058d0616c503b4b131a255a286823684141424261a385a1345626561416c6c40242e21d1e07c7e58edcb9df9037cecdedfd2cc792657708dfce9bf7decccefbdedbb70b0e793faf16166b41f0e0d1e35a1078b768fa3b393955d3d1d431248383c0b1f7f9c101ea04f01d1dbd4c07c5a204e640a63743d00390a103e0377d6fa606d90ffd0303a4c3cf274c9dac00043e7eeb0601d7c7ae911f6003e0cb07dafff589b6beafd09f8d35faf97589363ebfa02f6bb3f4fbdbb2d2fffdf181dd23394a02f864e9749a8687877d011bfb61eccd64a82fdd0351c215428eb854ca650cca0e5fa988e0c5d9dadc94c72a7a25edbaae94fd2ead6cecbfb35ba4c1fe0c4fcfc4585701ed4e0c92e003d2f09cef950e3155999613e3e20a41f035d46aba9bcf930e653825211001edce542e1f1293025f5d9e98b82dbb3d1a2280ce0f1dfc806c368b816003d88e1190c6102e5d11c03d400f146704111801f6191a1aa2d5d5655a7cbb2001193a7e034086ae991d7b8501a778500c635f7285206e86b80102c5a843d7e932fbf8e9d87652a3aa808cd7d5db6dca3e4c9a9979acd783d62b01b628421170dcc371907ae0fa5e4c121a9dae87aceb741936c04f07fd49421290dbc977bca79f6fb3e0b1e9feded1238626e73533343909c8d021480032745e03f4b563af302009e874637e0db23f07ee0a219f79d66364dbb9bea3ef82f5f58f29afc9a5bc2627019975badccc8e3dc380d3ea1dddcd0d5df1ffcbb09b7dc25eab2ac0ccaedf8db909b2cd158d41baa25ec7af415e13b55111d0cdc1b8dcbbd9e3b4d69af7391601fa6323440fe14d6092c0737e0b98378ecadcb93832a2ce52a954949c14415580e328b165ecf8438849e32cb75c1071a38c1a41e19ca552899a5501f47aa3e4af41ac03f018603449c1dcf4855f542009d00fc3242060d6b36cbe0560e7c021033ce711ba28431150ad5609190672b91c818842a140dbdbdbc4733d10fcafaf9320e1035f7d6d946445c0bbf72bb4f0664961eef93c01ac93f2eba5bab35fb87a872e8d4d495cb9799fc6efce4a40663d7cea16456ce23c9c994e3d7bfa4462fee55caa15d80f6bf89395fd61831e80cc7af68b58dcea38aa0294266182252061096f08d7564003250953d80a4858c21bc28d7d0534446c282c010621899bda0a485cca8d806d051884246e6a2b2071293702b615601092b8a9ad80c4a5dc08d856804148e2a6b602e296f2a0f1d80a08ca58dcfc6d05c42da341e3b1151094b1b8f9db0a885b4683c6632b20286371f3b71510b78c068dc7564050c6e2e66f2be0ac67b4dbf3ff030000ffff89063455000000064944415403007ffd019f418984b30000000049454e44ae426082"


VERSIONS_CONFIG: Dict[str, Dict[str, Any]] = {
    "Universal (1.9 – 26.3)": {
        "pack_format": 15,
        "supported_formats": [2, 99],
        "min_format": 2,
        "max_format": 99,
        "default_desc": "Custom Shield Pack (1.9 - 26.3 Universal)",
        "info": "Compatible with all Minecraft versions from 1.9 through 26.3."
    },
    "26.3 (2026 Update)": {
        "pack_format": 98,
        "supported_formats": [90, 99],
        "min_format": 90,
        "max_format": 99,
        "default_desc": "Custom Shield Pack (Minecraft 26.3)",
        "info": "Minecraft 26.3 format (Pack format 98)."
    },
    "26.2 (2026)": {
        "pack_format": 96,
        "supported_formats": [90, 99],
        "min_format": 90,
        "max_format": 99,
        "default_desc": "Custom Shield Pack (Minecraft 26.2)",
        "info": "Minecraft 26.2 format."
    },
    "26.1 (2026)": {
        "pack_format": 92,
        "supported_formats": [85, 95],
        "min_format": 85,
        "max_format": 95,
        "default_desc": "Custom Shield Pack (Minecraft 26.1)",
        "info": "Minecraft 26.1 format."
    },
    "1.21.4 (Tricky Trials)": {
        "pack_format": 46,
        "supported_formats": [42, 50],
        "min_format": 42,
        "max_format": 50,
        "default_desc": "Custom Shield Pack (Minecraft 1.21.4)",
        "info": "Minecraft 1.21.4 format."
    },
    "1.21.2 – 1.21.3": {
        "pack_format": 42,
        "supported_formats": [38, 45],
        "min_format": 38,
        "max_format": 45,
        "default_desc": "Custom Shield Pack (Minecraft 1.21.2 - 1.21.3)",
        "info": "Minecraft 1.21.2 - 1.21.3 format."
    },
    "1.21 – 1.21.1": {
        "pack_format": 34,
        "supported_formats": [30, 36],
        "min_format": 30,
        "max_format": 36,
        "default_desc": "Custom Shield Pack (Minecraft 1.21 - 1.21.1)",
        "info": "Minecraft 1.21 - 1.21.1 format."
    },
    "1.20.5 – 1.20.6": {
        "pack_format": 32,
        "supported_formats": [26, 33],
        "min_format": 26,
        "max_format": 33,
        "default_desc": "Custom Shield Pack (Minecraft 1.20.5 - 1.20.6)",
        "info": "Minecraft 1.20.5 - 1.20.6 format."
    },
    "1.20.3 – 1.20.4": {
        "pack_format": 22,
        "supported_formats": [18, 24],
        "min_format": 18,
        "max_format": 24,
        "default_desc": "Custom Shield Pack (Minecraft 1.20.3 - 1.20.4)",
        "info": "Minecraft 1.20.3 - 1.20.4 format."
    },
    "1.20.2": {
        "pack_format": 18,
        "supported_formats": [16, 20],
        "min_format": 16,
        "max_format": 20,
        "default_desc": "Custom Shield Pack (Minecraft 1.20.2)",
        "info": "Minecraft 1.20.2 format."
    },
    "1.20 – 1.20.1": {
        "pack_format": 15,
        "default_desc": "Custom Shield Pack (Minecraft 1.20 - 1.20.1)",
        "info": "Minecraft 1.20 - 1.20.1 format."
    },
    "1.19.4": {
        "pack_format": 13,
        "default_desc": "Custom Shield Pack (Minecraft 1.19.4)",
        "info": "Minecraft 1.19.4 format."
    },
    "1.19.3": {
        "pack_format": 12,
        "default_desc": "Custom Shield Pack (Minecraft 1.19.3)",
        "info": "Minecraft 1.19.3 format."
    },
    "1.19 – 1.19.2": {
        "pack_format": 9,
        "default_desc": "Custom Shield Pack (Minecraft 1.19 - 1.19.2)",
        "info": "Minecraft 1.19 - 1.19.2 format."
    },
    "1.18 – 1.18.2": {
        "pack_format": 8,
        "default_desc": "Custom Shield Pack (Minecraft 1.18 - 1.18.2)",
        "info": "Minecraft 1.18 - 1.18.2 format."
    },
    "1.17 – 1.17.1": {
        "pack_format": 7,
        "default_desc": "Custom Shield Pack (Minecraft 1.17 - 1.17.1)",
        "info": "Minecraft 1.17 - 1.17.1 format."
    },
    "1.16.2 – 1.16.5": {
        "pack_format": 6,
        "default_desc": "Custom Shield Pack (Minecraft 1.16.2 - 1.16.5)",
        "info": "Minecraft 1.16.2 - 1.16.5 format."
    },
    "1.15 – 1.16.1": {
        "pack_format": 5,
        "default_desc": "Custom Shield Pack (Minecraft 1.15 - 1.16.1)",
        "info": "Minecraft 1.15 - 1.16.1 format."
    },
    "1.13 – 1.14.4": {
        "pack_format": 4,
        "default_desc": "Custom Shield Pack (Minecraft 1.13 - 1.14.4)",
        "info": "Minecraft 1.13 - 1.14.4 format."
    },
    "1.11 – 1.12.2": {
        "pack_format": 3,
        "default_desc": "Custom Shield Pack (Minecraft 1.11 - 1.12.2)",
        "info": "Minecraft 1.11 - 1.12.2 format."
    },
    "1.9 – 1.10.2": {
        "pack_format": 2,
        "default_desc": "Custom Shield Pack (Minecraft 1.9 - 1.10.2)",
        "info": "Minecraft 1.9 - 1.10.2 format."
    }
}

RESOLUTIONS: Dict[str, int] = {
    "256x256 (4x HD)": 4,
    "512x512 (8x UHD)": 8,
    "1024x1024 (16x Max)": 16,
    "64x64 (1x Vanilla)": 1
}


def get_resource_path(relative_path: str) -> str:
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, relative_path)


def get_vanilla_shield_nopattern_64() -> Image.Image:
    local_path = get_resource_path("shield_base_nopattern.png")
    if os.path.exists(local_path):
        try:
            return Image.open(local_path).convert("RGBA")
        except Exception:
            pass
    raw = bytes.fromhex(VANILLA_SHIELD_NOPATTERN_HEX)
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def get_vanilla_shield_base_64() -> Image.Image:
    local_path = get_resource_path("shield_base.png")
    if os.path.exists(local_path):
        try:
            return Image.open(local_path).convert("RGBA")
        except Exception:
            pass
    raw = bytes.fromhex(VANILLA_SHIELD_BASE_HEX)
    return Image.open(io.BytesIO(raw)).convert("RGBA")


def process_user_image(
    user_img: Image.Image,
    target_width: int,
    target_height: int,
    scale_mode: str = "crop",
    resample_filter: int = Image.Resampling.LANCZOS
) -> Image.Image:
    img = user_img.convert("RGBA")
    src_w, src_h = img.size

    if scale_mode == "stretch":
        return img.resize((target_width, target_height), resample=resample_filter)

    target_aspect = target_width / target_height
    src_aspect = src_w / src_h

    if scale_mode == "crop":
        if src_aspect > target_aspect:
            new_crop_w = max(1, int(src_h * target_aspect))
            left = int((src_w - new_crop_w) / 2)
            cropped = img.crop((left, 0, left + new_crop_w, src_h))
        else:
            new_crop_h = max(1, int(src_w / target_aspect))
            top = int((src_h - new_crop_h) / 2)
            cropped = img.crop((0, top, src_w, top + new_crop_h))
        return cropped.resize((target_width, target_height), resample=resample_filter)

    elif scale_mode == "fit":
        if src_aspect > target_aspect:
            new_w = target_width
            new_h = max(1, int(target_width / src_aspect))
        else:
            new_h = target_height
            new_w = max(1, int(target_height * src_aspect))

        scaled = img.resize((new_w, new_h), resample=resample_filter)
        canvas = Image.new("RGBA", (target_width, target_height), (0, 0, 0, 0))
        offset_x = int((target_width - new_w) / 2)
        offset_y = int((target_height - new_h) / 2)
        canvas.paste(scaled, (offset_x, offset_y), scaled)
        return canvas

    return img.resize((target_width, target_height), resample=resample_filter)


def generate_shield_texture(
    user_image: Optional[Image.Image],
    multiplier: int = 4,
    keep_metal_rim: bool = True,
    scale_mode: str = "crop",
    filter_mode: str = "lanczos"
) -> Tuple[Image.Image, Image.Image]:
    resample_filter = (
        Image.Resampling.LANCZOS if filter_mode == "lanczos" else Image.Resampling.NEAREST
    )

    base_64 = get_vanilla_shield_nopattern_64()
    target_dim = 64 * multiplier

    if multiplier == 1:
        full_texture = base_64.copy()
    else:
        full_texture = base_64.resize((target_dim, target_dim), resample=Image.Resampling.NEAREST)

    if keep_metal_rim:
        x_start = 2 * multiplier
        y_start = 2 * multiplier
        dest_w = 10 * multiplier
        dest_h = 20 * multiplier
    else:
        x_start = 1 * multiplier
        y_start = 1 * multiplier
        dest_w = 12 * multiplier
        dest_h = 22 * multiplier

    if user_image is not None:
        processed_user_img = process_user_image(
            user_img=user_image,
            target_width=dest_w,
            target_height=dest_h,
            scale_mode=scale_mode,
            resample_filter=resample_filter
        )
        full_texture.paste(processed_user_img, (x_start, y_start), processed_user_img)

    front_x1 = 1 * multiplier
    front_y1 = 1 * multiplier
    front_x2 = 13 * multiplier
    front_y2 = 23 * multiplier
    front_preview = full_texture.crop((front_x1, front_y1, front_x2, front_y2))

    return full_texture, front_preview


def generate_pack_icon(front_preview: Image.Image) -> Image.Image:
    icon = Image.new("RGBA", (128, 128), (22, 24, 30, 255))
    draw = ImageDraw.Draw(icon)

    draw.rectangle([1, 1, 126, 126], outline=(45, 49, 60, 255), width=1)
    draw.rectangle([0, 0, 127, 127], outline=(14, 15, 18, 255), width=1)

    shield_h = 110
    shield_w = 60
    shield_scaled = front_preview.resize((shield_w, shield_h), resample=Image.Resampling.NEAREST)

    pos_x = int((128 - shield_w) / 2)
    pos_y = int((128 - shield_h) / 2)

    shadow = Image.new("RGBA", (shield_w, shield_h), (8, 9, 12, 140))
    icon.paste(shadow, (pos_x + 3, pos_y + 4), shadow)
    icon.paste(shield_scaled, (pos_x, pos_y), shield_scaled)

    return icon


def export_resource_pack(
    zip_path: str,
    full_texture: Image.Image,
    front_preview: Image.Image,
    version_key: str,
    pack_description: str,
    overwrite_banner_shield: bool = True
) -> None:
    ver_cfg = VERSIONS_CONFIG[version_key]

    pack_dict: Dict[str, Any] = {
        "pack_format": ver_cfg["pack_format"],
        "description": pack_description
    }

    if "supported_formats" in ver_cfg:
        pack_dict["supported_formats"] = ver_cfg["supported_formats"]
    if "min_format" in ver_cfg:
        pack_dict["min_format"] = ver_cfg["min_format"]
    if "max_format" in ver_cfg:
        pack_dict["max_format"] = ver_cfg["max_format"]

    mcmeta_content = json.dumps({"pack": pack_dict}, indent=2, ensure_ascii=False)

    pack_icon = generate_pack_icon(front_preview)
    icon_bytes = io.BytesIO()
    pack_icon.save(icon_bytes, format="PNG")

    texture_bytes = io.BytesIO()
    full_texture.save(texture_bytes, format="PNG")

    with zipfile.ZipFile(zip_path, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("pack.mcmeta", mcmeta_content.encode("utf-8"))
        zf.writestr("pack.png", icon_bytes.getvalue())
        zf.writestr("assets/minecraft/textures/entity/shield_base_nopattern.png", texture_bytes.getvalue())
        if overwrite_banner_shield:
            zf.writestr("assets/minecraft/textures/entity/shield_base.png", texture_bytes.getvalue())
        else:
            base_tex = get_vanilla_shield_base_64()
            base_bytes = io.BytesIO()
            base_tex.save(base_bytes, format="PNG")
            zf.writestr("assets/minecraft/textures/entity/shield_base.png", base_bytes.getvalue())


class ShieldCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Shield Creator")
        self.root.geometry("1120x760")
        self.root.minsize(960, 620)
        try:
            self.root.state('zoomed')
        except Exception:
            pass

        self.user_image = None
        self.user_image_path = None
        self.current_full_texture = None
        self.current_front_preview = None
        self.display_image = None
        self.preview_photo = None
        self.last_export_dir = None

        self.setup_ui()
        self.refresh_preview()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill="x", pady=(0, 10))

        ttk.Button(top_frame, text="Select Image File", command=self.select_image_file).pack(side="left")
        self.btn_reset = ttk.Button(top_frame, text="Reset to Default", command=self.reset_image, state="disabled")
        self.btn_reset.pack(side="left", padx=(5, 0))

        self.file_label = ttk.Label(top_frame, text="No image selected (Using default vanilla shield)")
        self.file_label.pack(side="left", padx=(10, 0))

        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        left_frame = ttk.Frame(content_frame, width=340)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)

        settings_frame = ttk.LabelFrame(left_frame, text="Shield Settings", padding=10)
        settings_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(settings_frame, text="Image Fitting:").pack(anchor="w", pady=(0, 2))
        self.combo_scale_mode = ttk.Combobox(settings_frame, values=["Crop", "Fit", "Stretch"], state="readonly")
        self.combo_scale_mode.set("Crop")
        self.combo_scale_mode.pack(fill="x", pady=(0, 6))
        self.combo_scale_mode.bind("<<ComboboxSelected>>", lambda _: self.refresh_preview())

        ttk.Label(settings_frame, text="Resolution:").pack(anchor="w", pady=(0, 2))
        self.combo_resolution = ttk.Combobox(settings_frame, values=list(RESOLUTIONS.keys()), state="readonly")
        self.combo_resolution.set("256x256 (4x HD)")
        self.combo_resolution.pack(fill="x", pady=(0, 6))
        self.combo_resolution.bind("<<ComboboxSelected>>", lambda _: self.refresh_preview())

        ttk.Label(settings_frame, text="Scaling Filter:").pack(anchor="w", pady=(0, 2))
        self.combo_filter = ttk.Combobox(settings_frame, values=["Lanczos (Smooth)", "Nearest (Pixel Art)"], state="readonly")
        self.combo_filter.set("Lanczos (Smooth)")
        self.combo_filter.pack(fill="x", pady=(0, 8))
        self.combo_filter.bind("<<ComboboxSelected>>", lambda _: self.refresh_preview())

        self.rim_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Preserve Iron Rim & Rivets", variable=self.rim_var, command=self.refresh_preview).pack(anchor="w", pady=(0, 4))

        self.banner_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(settings_frame, text="Overwrite Banner Shields (shield_base.png)", variable=self.banner_var).pack(anchor="w")

        pack_frame = ttk.LabelFrame(left_frame, text="Pack Configuration", padding=10)
        pack_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(pack_frame, text="Target Minecraft Version:").pack(anchor="w", pady=(0, 2))
        self.combo_version = ttk.Combobox(pack_frame, values=list(VERSIONS_CONFIG.keys()), state="readonly")
        self.combo_version.set("Universal (1.9 – 26.3)")
        self.combo_version.pack(fill="x", pady=(0, 2))
        self.combo_version.bind("<<ComboboxSelected>>", self._on_version_changed)

        self.lbl_version_hint = ttk.Label(pack_frame, text=VERSIONS_CONFIG["Universal (1.9 – 26.3)"]["info"], wraplength=300)
        self.lbl_version_hint.pack(anchor="w", pady=(2, 6))

        ttk.Label(pack_frame, text="Pack Name:").pack(anchor="w", pady=(0, 2))
        self.entry_pack_name = ttk.Entry(pack_frame)
        self.entry_pack_name.insert(0, "CustomShieldPack")
        self.entry_pack_name.pack(fill="x", pady=(0, 6))

        ttk.Label(pack_frame, text="In-Game Description:").pack(anchor="w", pady=(0, 2))
        self.entry_pack_desc = ttk.Entry(pack_frame)
        self.entry_pack_desc.insert(0, "Custom Shield Pack (1.9 - 26.3 Universal)")
        self.entry_pack_desc.pack(fill="x")

        process_frame = ttk.LabelFrame(left_frame, text="Export", padding=10)
        process_frame.pack(fill="x")

        ttk.Button(process_frame, text="Export Resource Pack (.zip)", command=self.export_pack).pack(fill="x", pady=(0, 5))
        ttk.Button(process_frame, text="Save Texture (.png)", command=self.export_texture_only).pack(fill="x", pady=(0, 5))

        self.btn_open_folder = ttk.Button(process_frame, text="Open Export Folder", command=self.open_export_folder, state="disabled")
        self.btn_open_folder.pack(fill="x", pady=(0, 6))

        self.status_label = ttk.Label(process_frame, text="Ready to export")
        self.status_label.pack(anchor="w")

        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        preview_header = ttk.Frame(right_frame)
        preview_header.pack(fill="x", pady=(0, 5))

        ttk.Label(preview_header, text="Image Preview:").pack(side="left")
        self.combo_view = ttk.Combobox(preview_header, values=["Shield Front", "Texture Sheet"], state="readonly", width=16)
        self.combo_view.set("Shield Front")
        self.combo_view.pack(side="right")
        self.combo_view.bind("<<ComboboxSelected>>", lambda _: self.refresh_preview())

        image_frame = ttk.Frame(right_frame)
        image_frame.pack(fill="both", expand=True, pady=(5, 0))

        self.canvas = tk.Canvas(image_frame, bg="white", highlightthickness=1, highlightbackground="#d0d0d0")
        v_scrollbar = ttk.Scrollbar(image_frame, orient="vertical", command=self.canvas.yview)
        h_scrollbar = ttk.Scrollbar(image_frame, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")

        self.canvas.bind("<Configure>", lambda e: self._draw_canvas_content())

        self.info_label = ttk.Label(right_frame, text="")
        self.info_label.pack(anchor="w", pady=(5, 0))

    def _on_version_changed(self, event=None):
        choice = self.combo_version.get()
        cfg = VERSIONS_CONFIG.get(choice, {})
        self.lbl_version_hint.config(text=cfg.get("info", ""))
        self.refresh_preview()

    def select_image_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("WebP files", "*.webp"),
                ("All files", "*.*")
            ]
        )
        if not file_path:
            return

        try:
            loaded_img = Image.open(file_path)
            loaded_img.load()
            self.user_image = loaded_img
            self.user_image_path = file_path

            filename = os.path.basename(file_path)
            orig_w, orig_h = loaded_img.size
            self.file_label.config(text=f"File: {filename} ({orig_w}x{orig_h} px)")
            self.btn_reset.config(state="normal")

            clean_name = os.path.splitext(filename)[0].replace(" ", "_")
            self.entry_pack_name.delete(0, tk.END)
            self.entry_pack_name.insert(0, f"Shield_{clean_name}")

            self.refresh_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Error opening image: {str(e)}")

    def reset_image(self):
        self.user_image = None
        self.user_image_path = None
        self.file_label.config(text="No image selected (Using default vanilla shield)")
        self.btn_reset.config(state="disabled")
        self.entry_pack_name.delete(0, tk.END)
        self.entry_pack_name.insert(0, "CustomShieldPack")
        self.refresh_preview()

    def get_current_settings(self) -> Dict[str, Any]:
        res_str = self.combo_resolution.get()
        multiplier = RESOLUTIONS.get(res_str, 4)
        scale_val = self.combo_scale_mode.get()
        if "Crop" in scale_val:
            scale_mode = "crop"
        elif "Stretch" in scale_val:
            scale_mode = "stretch"
        else:
            scale_mode = "fit"

        filter_val = self.combo_filter.get()
        filter_mode = "lanczos" if "Lanczos" in filter_val else "nearest"

        return {
            "multiplier": multiplier,
            "keep_rim": self.rim_var.get(),
            "scale_mode": scale_mode,
            "filter_mode": filter_mode,
            "version_key": self.combo_version.get(),
            "pack_name": self.entry_pack_name.get().strip() or "CustomShieldPack",
            "pack_desc": self.entry_pack_desc.get().strip() or "Custom Shield Resource Pack",
            "overwrite_banner": self.banner_var.get()
        }

    def _draw_canvas_content(self):
        if not hasattr(self, 'display_image') or self.display_image is None:
            return

        cw = max(self.canvas.winfo_width(), self.display_image.width + 40)
        ch = max(self.canvas.winfo_height(), self.display_image.height + 40)
        self.canvas.configure(scrollregion=(0, 0, cw, ch))

        self.canvas.delete("all")
        self.preview_photo = ImageTk.PhotoImage(self.display_image)
        self.canvas.create_image(
            int(cw / 2),
            int(ch / 2),
            anchor="center",
            image=self.preview_photo
        )

    def refresh_preview(self):
        settings = self.get_current_settings()
        multiplier = settings["multiplier"]
        keep_rim = settings["keep_rim"]

        full_tex, front_prev = generate_shield_texture(
            user_image=self.user_image,
            multiplier=multiplier,
            keep_metal_rim=keep_rim,
            scale_mode=settings["scale_mode"],
            filter_mode=settings["filter_mode"]
        )

        self.current_full_texture = full_tex
        self.current_front_preview = front_prev

        view_mode = self.combo_view.get()
        if "Front" in view_mode:
            target_h = 440
            target_w = int(target_h * (12 / 22))
            self.display_image = front_prev.resize((target_w, target_h), resample=Image.Resampling.NEAREST)
        else:
            dim = 400
            self.display_image = full_tex.resize((dim, dim), resample=Image.Resampling.NEAREST)

        self._draw_canvas_content()

        total_dim = 64 * multiplier
        front_area_w = 10 * multiplier if keep_rim else 12 * multiplier
        front_area_h = 20 * multiplier if keep_rim else 22 * multiplier
        rim_str = "Bordered" if keep_rim else "Full Face"
        v_cfg = VERSIONS_CONFIG.get(settings["version_key"], {})
        pf = v_cfg.get("pack_format", 15)

        self.info_label.config(
            text=f"Texture: {total_dim}x{total_dim} px ({multiplier}x) | Face: {front_area_w}x{front_area_h} px ({rim_str}) | Pack Format: {pf}"
        )

    def export_pack(self):
        if self.current_full_texture is None or self.current_front_preview is None:
            self.refresh_preview()

        settings = self.get_current_settings()
        clean_pack_name = "".join(
            c for c in settings["pack_name"] if c.isalnum() or c in ("-", "_")
        ) or "CustomShieldPack"

        v_key = settings["version_key"]
        v_tag = "1.9-26.3_Universal" if "Universal" in v_key else v_key.split(" ")[0]
        default_zip_name = f"{clean_pack_name}_{v_tag}.zip"

        save_path = filedialog.asksaveasfilename(
            title="Save Resource Pack as ZIP",
            defaultextension=".zip",
            initialfile=default_zip_name,
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")]
        )

        if not save_path:
            return

        try:
            export_resource_pack(
                zip_path=save_path,
                full_texture=self.current_full_texture,
                front_preview=self.current_front_preview,
                version_key=settings["version_key"],
                pack_description=settings["pack_desc"],
                overwrite_banner_shield=settings["overwrite_banner"]
            )

            self.last_export_dir = os.path.dirname(os.path.abspath(save_path))
            self.status_label.config(text=f"Saved: {os.path.basename(save_path)}")
            self.btn_open_folder.config(state="normal")

            messagebox.showinfo(
                "Success",
                f"Resource Pack saved successfully!\n\n"
                f"File: {save_path}\n\n"
                f"To install:\n"
                f"Place this .zip file in your .minecraft/resourcepacks folder."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Error saving Resource Pack: {str(e)}")

    def export_texture_only(self):
        if self.current_full_texture is None:
            self.refresh_preview()

        settings = self.get_current_settings()
        clean_name = "".join(
            c for c in settings["pack_name"] if c.isalnum() or c in ("-", "_")
        ) or "shield_texture"

        default_png_name = f"{clean_name}.png"

        save_path = filedialog.asksaveasfilename(
            title="Save Texture as PNG",
            defaultextension=".png",
            initialfile=default_png_name,
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )

        if not save_path:
            return

        try:
            self.current_full_texture.save(save_path, format="PNG")
            self.last_export_dir = os.path.dirname(os.path.abspath(save_path))
            self.status_label.config(text=f"Saved: {os.path.basename(save_path)}")
            self.btn_open_folder.config(state="normal")
            messagebox.showinfo("Success", f"Texture saved:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving texture: {str(e)}")

    def open_export_folder(self):
        if self.last_export_dir and os.path.exists(self.last_export_dir):
            if sys.platform == "win32":
                os.startfile(self.last_export_dir)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", self.last_export_dir])
            else:
                subprocess.Popen(["xdg-open", self.last_export_dir])


def main():
    root = tk.Tk()
    app = ShieldCreatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
