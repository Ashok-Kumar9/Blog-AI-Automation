export const imageStorage = {
  dbPromise: new Promise((resolve, reject) => {
    const request = indexedDB.open('blog-images-db', 1);
    request.onupgradeneeded = (e) => {
      e.target.result.createObjectStore('imagesStore');
    };
    request.onsuccess = (e) => resolve(e.target.result);
    request.onerror = (e) => reject(e.target.error);
  }),

  async getMap() {
    try {
      const db = await this.dbPromise;
      return new Promise((resolve, reject) => {
        const tx = db.transaction('imagesStore', 'readonly');
        const request = tx.objectStore('imagesStore').get('generated_images_map');
        request.onsuccess = () => resolve(request.result || {});
        request.onerror = () => reject(request.error);
      });
    } catch (err) {
      console.warn("IndexedDB getMap failed", err);
      return {};
    }
  },

  async setMap(map) {
    try {
      const db = await this.dbPromise;
      return new Promise((resolve, reject) => {
        const tx = db.transaction('imagesStore', 'readwrite');
        const request = tx.objectStore('imagesStore').put(map, 'generated_images_map');
        request.onsuccess = () => resolve();
        request.onerror = () => reject(request.error);
      });
    } catch (err) {
      console.warn("IndexedDB setMap failed", err);
    }
  }
};
